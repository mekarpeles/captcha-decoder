# -*- coding: utf-8 -*-

"""
    tests
    ~~~~~
    Test cases for the decaptcha package

    :copyright: (c) 2012 by Mek
    :license: see LICENSE for more details.
"""

import os.path
import unittest
from PIL import Image
import decaptcha

TEST_IMG_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir, 'tests', 'images'))
TEST_CAPTCHA_IMG = os.path.join(TEST_IMG_DIR, 'captcha.gif')
TEST_CHANNEL_IMG = os.path.join(TEST_IMG_DIR, 'channel.gif')
TEST_SEGMENT_IMG = lambda i: os.path.join(TEST_IMG_DIR, 'segment%s.gif' % i)
EXPECTED_HISTOGRAM = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0,
    2, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 2, 0, 0, 0, 1, 2, 0, 1, 0, 0, 1, 0, 2, 0, 0, 1, 0, 0, 2, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 1, 0, 3,
    2, 132, 1, 1, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 15, 0, 1, 0, 1, 0, 0,
    8, 1, 0, 0, 0, 0, 1, 6, 0, 2, 0, 0, 0, 0, 18, 1, 1, 1, 1, 1, 2, 365,
    115, 0, 1, 0, 0, 0, 135, 186, 0, 0, 1, 0, 0, 0, 116, 3, 0, 0, 0, 0, 0,
    21, 1, 1, 0, 0, 0, 2, 10, 2, 0, 0, 0, 0, 2, 10, 0, 0, 0, 0, 1, 0, 625
    ]
EXPECTED_DOMINANT_COLORS = [
    (255, 625), (212, 365), (220, 186), (219, 135), (169, 132), (227, 116),
    (213, 115), (234, 21), (205, 18), (184, 15)
    ]
EXPECTED_REGIONS = [
    (6, 14), (15, 25), (27, 35), (37, 46), (48, 56), (57, 67)
    ]
EXPECTED_OUTPUT = (1.0, '7')


class CaptchaDecoderTest(unittest.TestCase):

    def setUp(self):
        self.captcha = decaptcha.Captcha(TEST_CAPTCHA_IMG)

    def test_histogram(self):
        self.assertTrue(self.captcha.histogram == EXPECTED_HISTOGRAM,
                        "Captcha histogram different from expected")

    def test_prominant_colors(self):
        self.assertTrue(self.captcha.prominant_colors(n=10, white=True) ==
                        EXPECTED_DOMINANT_COLORS,
                        "Captcha's dominant colors differ from expected")

    def test_channels(self):
        channel = decaptcha.monochrome(self.captcha.channel(220, 227))
        print(channel.histogram())
        self.assertTrue(channel.histogram() ==
                        Image.open(TEST_CHANNEL_IMG).histogram(),
                        "Channel sample did not match expected image")

    def test_regions(self):
        sample = decaptcha.monochrome(self.captcha.channel(220, 227))
        regions = self.captcha.regions(sample)
        self.assertTrue(regions == EXPECTED_REGIONS,
                        "Expected regions %s, instead got %s"
                        % (EXPECTED_REGIONS, regions))

    def test_segmentation(self):
        """Note, in the test cases of the original publication
        (http://tinyurl.com/phvggox), output segments #3 and #5 (which
        are both the number 9) are mistakenly swapped.
        """
        sample = decaptcha.monochrome(self.captcha.channel(220, 227))
        segments = self.captcha.segments(sample, crop=False)
        for i, segment in enumerate(segments):
            EXPECTED_SEGMENT = Image.open(TEST_SEGMENT_IMG(i+1))
            self.assertTrue(segment.histogram() ==
                            EXPECTED_SEGMENT.histogram(),
                            "Segment #%s is wrong." % (i+1))

    def test_guess_character(self):
        sample = decaptcha.monochrome(self.captcha.channel(220, 227))
        regions = self.captcha.regions(sample)
        segment = self.captcha.segment(sample, regions[0], crop=False)
        exp_seg = Image.open(TEST_SEGMENT_IMG(1))
        self.assertTrue(segment.histogram() == exp_seg.histogram(),
                        "Segment is wrong")
        predictions = self.captcha.guess_character(segment)
        self.assertTrue(predictions[0] == EXPECTED_OUTPUT,
                        "Expected %s, got %s" %
                        (EXPECTED_OUTPUT, predictions[0]))

    def test_decoder(self):
        self.captcha.decode()
