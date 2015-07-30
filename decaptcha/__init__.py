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

import sys
from .decoder import Captcha  # NOQA
from .decoder import trim, channel, monochrome, regions, decode  # NOQA
from .cli import main

if __name__ == '__main__':
    sys.exit(main())
