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
from operator import itemgetter
from math import sqrt
from PIL import Image, ImageChops
from io import BytesIO

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

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


def trim(im, color=WHITE):
    """Tims image to remove excess color (default: whitespace)"""
    bg = Image.new(im.mode, im.size, WHITE)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    return im.crop(diff.getbbox())


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
        if sum([im.getpixel((col, row)) is not WHITE
                for row in range(height)]) >= threshold:
            start = start if start else col
        elif start:
            regions.append((start, col))
            start = None  # reset start
    return regions


def similarity(im1, im2, equalize=False):
    """Takes in two images, vectorizes them into concordance
    dictionaries and spits out a number from 0 to 1 indicating how
    related they are. 0 means no relation and 1 indicates they are the
    same.

    params:
        stretch - stretch im2 to be the same dimensions as 1
    """
    def scale(im1, im2):
        """Scales the image with the greater height to match the one
        with the smaller height
        """
        if im1.size[1] > im2.size[1]:
            return im1.resize(im2.size, Image.ANTIALIAS), im2
        elif im1.size[1] < im2.size[1]:
            return im1, im2.resize(im1.size, Image.ANTIALIAS)
        return im1, im2

    def vectorize(im):
        """im.getdata returns the contents of an image as a flattened
        sequence object containing pixel values.
        """
        d1 = {}
        for count, i in enumerate(im.getdata()):
            d1[count] = i
        return d1

    def magnitude(concordance):
        return sqrt(sum(count ** 2 for word, count in concordance.items()))

    c1, c2 = [vectorize(im) for im in
              (scale(im1, im2) if equalize else (im1, im2))]
    topvalue = 0
    for word, count in c1.items():
        if word in c2:
            topvalue += count * c2[word]
    return topvalue / (magnitude(c1) * magnitude(c2))


class Captcha(object):

    def __init__(self, imgpath):
        self.imgpath = imgpath

    @property
    def im(self):
        """Fetches captcha's image from disk or url"""
        try:
            im = Image.open(self.imgpath)
        except:
            im = Image.open(BytesIO(urlopen(self.imgpath).read()))
        return self.gif(im)

    @property
    def histogram(self):
        with self.im as im:
            return im.histogram()

    def decode(self, channels=3, limit=3, threshold=0, tolerance=3,
               _min=0, _max=245):
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
        colors = [color for color, _ in self
                  .prominant_colors(n=channels, _min=_min, _max=_max)]
        sample = monochrome(self.channel(*colors))
        return [self.guess_character(segment, limit=limit, threshold=threshold)
                for segment in self.segments(sample, tolerance=tolerance)]

    def prominant_colors(self, n=5, _min=0, _max=256):
        """Calculates the n most prominant colors of an image as an
        ordered list of (color, frequency) tuples.

        params:
            n - limit the number of colors to `n`
            _min - exclude any colors below this number (filter
                   out dark colors, like black/0)
            _max - exclude any colors above this number (filter out
                   light colors, like white/256)

        XXX consider sorted(im.getcolors(n), reverse=True)
        """
        hist = self.histogram[_min:_max]
        return sorted([(c, f) for c, f in enumerate(hist)],
                      key=itemgetter(1), reverse=True)[:n]

    def channel(self, *colors, **kwargs):
        """Composes an image with the same dimensions as `im` but
        draws only pixels of the specified colors on a `bg` colored
        background.
        """
        with self.im as im:
            return channel(im, *colors, **kwargs)

    @staticmethod
    def gif(im):
        """Converts captcha to a GIF (makes things easier since it has
        255 colors) and finds the most prominent colors in the image
        """
        return im if im.mode is 'P' else im.convert('P')

    @classmethod
    def segments(cls, im, tolerance=3, crop=True):
        """Discover """
        return [cls.segment(im, region, crop=crop) for
                region in regions(im, threshold=tolerance)]

    @classmethod
    def segment(cls, im, region, crop=True):
        """Returns a cropped image segment (hopefully of an
        alphanumeric character) within the range of the region
        """
        start, end = 0, 1
        segment = im.crop((region[start], 0, region[end], im.size[1]))
        return trim(segment) if crop else segment

    @staticmethod
    def guess_character(im, threshold=0, limit=None):
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
                guess = similarity(im, im2, equalize=True)
                if guess >= threshold:
                    guesses.append((guess, symbol))
        return sorted(guesses, reverse=True)[:limit]


def decode(captcha, channels=1, limit=3, threshold=0, tolerance=3,
           _min=0, _max=256):
    """Backward compatible method for decoding a captcha"""
    return Captcha(captcha).decode(
        channels=channels,
        limit=limit,
        threshold=threshold,
        tolerance=tolerance,
        _min=_min, _max=_max)
