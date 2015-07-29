import os.path
import unittest
import decaptcha


class CaptchaDecoderTest(unittest.TestCase):

    def test_crack(self):
        captcha = os.path.join(decaptcha.DATA_PATH, 'captcha.gif')
        decaptcha.crack.decode(captcha)
