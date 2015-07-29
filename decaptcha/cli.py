#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from . import crack, __title__, __version__


def argparser():
    """Creates a command line ArgumentParser for decaptcha."""
    parser = argparse.ArgumentParser(description=__title__)
    parser.add_argument('-v', help="Displays the decaptcha version",
                        action="version", version="%s v%s"
                        % (__title__, __version__))
    parser.add_argument('captcha', nargs='?', metavar='<img>',
                        help='Enter the path of a captcha img file (.jpg)')
    parser.add_argument('--out', nargs='*', default='',
                        help='Directory where output imgs should be '
                        'saved. (default: $PWD)')
    parser.add_argument('--verbose', '-vv', action='count')
    return parser


def main():
    parser = argparser()
    args = parser.parse_args()

    if not args.captcha:
        raise ValueError('No captcha input image provided')

    captcha = args.captch if args.captcha.startswith(os.sep) else\
        os.path.join(os.getcwd(), args.captcha)

    guesses = crack.decode(captcha, outpath=args.out)
    print([guess for guess in guesses] if args.verbose else
          [guess[0] for guess in guesses])


if __name__ == "__main__":
    main()
