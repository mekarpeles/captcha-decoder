import unittest
from decaptcha import crack

class Captcha_Decoder_Test(unittest.TestCase):
    
    def test_crack():
        crack.crack_captcha("captcha.jpg")
        
