#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from . import Captcha, __title__, __version__


def threshold(x):
    x = float(x)
    if 1 > x < 0:
        raise argparse.ArgumentTypeError(
            "Threshold must be a value between 0 and 1.")
    return x


def argparser():
    """Creates a command line ArgumentParser for decaptcha."""
    parser = argparse.ArgumentParser(description=__title__)
    parser.add_argument('-v', help='Displays the decaptcha version',
                        action='version', version='%s v%s'
                        % (__title__, __version__))
    parser.add_argument('captcha', nargs='?', metavar='<img>',
                        help='Enter the filesystem path or url '
                        'of a captcha image')
    parser.add_argument('-l', '--limit', dest='limit', help='Package url',
                        type=int, default=3)
    parser.add_argument('-c', '--channels', dest='channels',
                        help='The number of prominant color channels to keep',
                        type=int, default=3)
    parser.add_argument('-t', '--threshold', dest='threshold',
                        help='Accuracy threshold for matching decimal [0-1]',
                        type=threshold, default=0)
    parser.add_argument('--min', dest='min', type=int, default=0,
                        help='Filter out colors darker than this [0-256]')
    parser.add_argument('--max', dest='max', type=int, default=230,
                        help='Filter out colors light than this [0-256]')
    parser.add_argument('-o', '--tolerance', dest='tolerance', type=int,
                        default=3, help='Pixel tolerance for character '
                        'segmentation. Higher is more lenient/greedy, '
                        'lower is strict.')
    return parser


def prettyprint(guesses):
    regions = len(guesses)
    for i, guess in enumerate(guesses):
        print('Character %s of %s:' % (i + 1, regions))
        for result in guess:
            confidence, symbol = result
            print('\t%s (%s confidence)' % (symbol, confidence))


def main():
    parser = argparser()
    args = parser.parse_args()

    if not args.captcha:
        raise ValueError('No captcha input image provided')

    prettyprint(Captcha(args.captcha).decode(channels=args.channels,
                                             limit=args.limit,
                                             threshold=args.threshold,
                                             tolerance=args.tolerance,
                                             _min=args.min,
                                             _max=args.max))


if __name__ == "__main__":
    main()
