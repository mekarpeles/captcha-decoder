# -*- coding: utf-8 -*-

"""
   decaptcha
   ~~~~~~~~~

   Basic Captcha Cracker
"""

__version__ = '0.0.1'
__author__ = [
    'Mek <michael.karpeles@gmail.com>'
]
__license__ = 'see LICENSE (creative commons)'
__contributors__ = 'see AUTHORS'
__title__ = 'Python captcha cracking utility'


import os
import sys
from .cli import main

DATA_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir, 'data'))

if __name__ == '__main__':
    sys.exit(main())
