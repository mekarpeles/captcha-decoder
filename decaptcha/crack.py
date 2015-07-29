# -*- coding: utf-8 -*-

"""
    crack.py
    ~~~~~~~~

    This module takes captcha images as input and partitions them into
    n new images, 1 image per character found within the captcha.

    Original by bboyte01@gmail.com, http://www.wausita.com/captcha/

    :copyright: (c) 2012 by Abel and Mek
    :license: Creative Commons, see LICENSE for more details.
"""

import os
import time
from PIL import Image
from .util import build_imgset, buildvector, crop_white

IMAGESET = build_imgset()


def relation(concordance1, concordance2):
    """
    """
    relevance = 0
    for word, count in concordance1.iteritems():
        if word in concordance2 and count == concordance2[word]:
            if not count:
                relevance += 5 if not count else 1
    return float(relevance)/float(len(concordance2))


def preprocess_captcha(captcha, timestamp, outpath=''):
    """
    """
    im = Image.open(captcha).convert('P')
    im2 = Image.new('P', im.size, 255)
    temp = {}
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            temp[pix] = pix
            if pix < 10:  # these are the numbers to get
                im2.putpixel((y, x), 0)
    _fname = '%s_output.gif' % timestamp
    im2.save('%s/%s' % (outpath, _fname) if outpath else _fname)
    return im2


def find_partitions(im):
    """Find discrete partitions within the preprocessed captcha to find
    regions containing individual characters. Returns an accumuated list
    of (start, end) coordinates for this region. Partitions are
    calculated based on the existence of characters within the image, as
    determined by surrounding white space.
    """
    letters = []
    inletter = False
    foundletter = False
    start, end = 0, 0

    for y in range(im.size[0]):  # slice across
        for x in range(im.size[1]):  # slice down
            pix = im.getpixel((y, x))
            if not pix == 255:
                inletter = True

        if not foundletter and inletter:
            foundletter = True
            start = y

        if foundletter and not inletter:
            foundletter = False
            end = y
            letters.append((start, end))
        inletter = False
    return letters


def segment_captcha(im, partitions, timestamp, outpath=''):
    """Iterates over all discrete segments containing characters found
    within the captcha, crops them and saved them as individual icons
    """
    segments = []
    for count, partition in enumerate(partitions):
        _fname = '%s_%s.gif' % (timestamp, count)
        segment_filename = '%s/%s' % (outpath, _fname) if outpath else _fname
        segment = crop_white(im.crop((partition[0], 0,
                                      partition[1], im.size[1])))
        segment.save(segment_filename)
        segments.append(segment)
    return segments


def guess_characters(segments):
    """Loops over each segment and attempts to guess what character is
    contained within the cropped img
    """
    captcha = []
    for segment in segments:
        guess = []
        for icon in IMAGESET:
            for x, y in icon.iteritems():
                if len(y):
                    for option in y:
                        s = segment.resize(option.size)
                        guess.append((relation(buildvector(option),
                                               buildvector(s)), x))
        guess.sort(reverse=True)
        captcha.append(guess)
    return captcha


def decode(captcha, outpath=''):
    """Decodes a captcha"""
    if outpath:
        outpath = outpath.rstrip('/')
        if not os.path.exists(outpath):
            os.makedirs(outpath)
    timestamp = int(time.time())
    im = preprocess_captcha(captcha, timestamp, outpath=outpath)
    parts = find_partitions(im)
    segments = segment_captcha(im, parts, timestamp, outpath=outpath)
    return guess_characters(segments)
