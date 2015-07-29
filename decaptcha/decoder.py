# -*- coding: utf-8 -*-

"""
    crack.py
    ~~~~~~~~

    This module takes captcha images as input and partitions them into
    n new images, 1 image per character found within the captcha.

    Original Code (http://tinyurl.com/puq6alb) by bboyte01@gmail.com
    https://web.archive.org/web/20121012023114/http://www.wausita.com/captcha/
    http://www.wausita.com/captcha/

    :copyright: (c) 2012 by Mek
    :license: see LICENSE for more details.
"""

import os
import string
from math import sqrt
from PIL import Image
from operator import itemgetter

SYMBOLS = list(string.ascii_lowercase + string.digits)
ICONS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'iconset'))
IMAGESET = []
WHITE = 255


def imageset():
    """Loads icons of various characters"""
    imageset = []
    for symbol in SYMBOLS:
        for imfile in os.listdir(os.path.join(ICONS_PATH, symbol)):
            path = os.path.join(ICONS_PATH, symbol, imfile)
            imageset.append({symbol: Image.open(path)})
    return imageset


def autocrop(img, color=WHITE):
    """Crops image to remove excess color (default: whitespace)"""
    min_coord = img.size[1] + 10
    max_coord = -1
    for y in range(img.size[0]):  # slice across
        for x in range(img.size[1]):  # slice down
            pix = img.getpixel((y, x))
            if pix != color:
                min_coord = min(min_coord, x)
                max_coord = max(max_coord, x)
    return img.crop((0, min_coord, img.size[0], max_coord))


def channel(im, *colors, **kwargs):
    """Composes an new image with the same dimensions as `im` but
    draws only pixels of the specified color channels on a `bg`
    colored background.
    """
    bg = kwargs.get('bg', WHITE)
    sample = Image.new('P', im.size, bg)
    width, height = im.size
    for col in range(width):
        for row in range(height):
            pixel = im.getpixel((col, row))
            if pixel in colors:
                sample.putpixel((col, row), pixel)
    return sample


def monochrome(im, threshold=255):
    """Converts all colors in gif image which are less than threshold
    to black"""
    return im.point(lambda x: 0 if x < 255 else 255, '1')


def regions(im, threshold=1):
    """Iterates over the columns of an image from left-to-right and
    composes an ordered list of (start, end) column ranges referring
    to discrete, contiguous columns which contain at least `threshold`
    non-white pixel.
    """
    regions = []
    start = None
    width, height = im.size
    for col in range(width):
        # if column contains at least one pixel
        if any(im.getpixel((col, row)) is not WHITE
               for row in range(height)):
            start = start if start else col
        elif start:
            regions.append((start, col))
            start = None  # reset start
    return regions


def similarity(im1, im2):
    """Takes in two images, vectorizes them into concordance
    dictionaries and spits out a number from 0 to 1 indicating how
    related they are. 0 means no relation and 1 indicates they are the
    same."""
    def vectorize(im):
        d1 = {}
        # im.getdata returns the contents of an image as a flattened
        # sequence object containing pixel values.
        for count, i in enumerate(im.getdata()):
            d1[count] = i
        return d1

    def magnitude(concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return sqrt(total)

    concordance1, concordance2 = vectorize(im1), vectorize(im2)
    topvalue = 0
    for word, count in concordance1.items():
        if word in concordance2:
            topvalue += count * concordance2[word]
    return topvalue / (magnitude(concordance1) * magnitude(concordance2))


class Captcha(object):

    def __init__(self, imgpath):
        self.imgpath = imgpath

    def decode(self, channels=3, limit=3, threshold=.8):
        """Attempts to decode a captcha by:

        - Finding the `n` most prominant colors in the image
        - Sampling the captcha into `n` images, each discretely composed
          of a differnet prominant colors.
        - Segmenting each sample into regions of contiguous columns
          containing any pixels pixelation (which are hopefully
          equates to individual alphanumeric characters), and finally
        - Guessing which character appears in each segment

        XXX Prettier output and organizing of results required
        """
        colors = [color for color, _ in self.prominant_colors(n=channels)]
        sample = monochrome(self.channel(*colors))
        return [self.guess_character(
                segment, limit=limit, threshold=threshold
                ) for segment in self.segments(sample)]

    @property
    def histogram(self):
        with self.gif(Image.open(self.imgpath)) as im:
            return im.histogram()

    def prominant_colors(self, n=10, white=False):
        """Calculates the n most prominant colors of an image as an
        ordered list of (color, frequency) tuples.

        XXX consider sorted(im.getcolors(n), reverse=True)
        """
        hist = self.histogram if white else self.histogram[:255]
        return sorted([(c, f) for c, f in enumerate(hist)],
                      key=itemgetter(1), reverse=True)[:n]

    def channel(self, *colors, **kwargs):
        """Composes an image with the same dimensions as `im` but
        draws only pixels of the specified colors on a `bg` colored
        background.
        """
        with self.gif(Image.open(self.imgpath)) as im:
            return channel(im, *colors, **kwargs)

    @staticmethod
    def gif(im):
        """Converts captcha to a GIF (makes things easier since it has
        255 colors) and finds the most prominent colors in the image
        """
        return im if im.mode is 'P' else im.convert('P')

    @classmethod
    def segments(cls, im, crop=False):
        """Discover """
        return [cls.segment(im, region, crop=crop) for
                region in cls.regions(im)]

    @staticmethod
    def segment(im, region, crop=True):
        """Returns a cropped image segment (hopefully of an
        alphanumeric character) within the range of the region
        """
        start, end = 0, 1
        segment = im.crop((region[start], 0, region[end], im.size[1]))
        return autocrop(segment) if crop else segment

    @classmethod
    def regions(cls, im):
        return regions(im)

    @staticmethod
    def guess_character(im, threshold=.80, limit=None):
        """Guess alphanumeric character in image using Basic Vector
        Space Search algorithm.

        http://la2600.org/talks/files/20040102/Vector_Space_Search_Engine_Theory.pdf
        """
        global IMAGESET  # lazy-ish style iconset loading
        if not IMAGESET:
            IMAGESET = imageset()

        guesses = []
        for icon in IMAGESET:
            for symbol, im2 in icon.items():
                guess = similarity(im2, im)
                if guess > threshold:
                    guesses.append((similarity(im2, im), symbol))
        return sorted(guesses, reverse=True)[:limit]


def decode(captcha, channels=1, limit=3, threshold=.8):
    """Backward compatible method for decoding a captcha"""
    return Captcha(captcha).decode(
        channels=channels, limit=limit, threshold=threshold)
