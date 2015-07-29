import unittest

from decaptcha import crack


class CaptchaDecoderTest(unittest.TestCase):

    def test_crack(self):
        crack.decode('captcha.jpg')
