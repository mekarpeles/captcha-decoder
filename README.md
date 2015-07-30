captcha-decoder
===============

![Build Status](https://travis-ci.org/mekarpeles/captcha-decoder.png)

This module takes a captcha (image) as input, attempts to partition it into discrete segments, each (it hopes) containing a single symbol, and then runs basic vector space search to determine the similarity of each symbol against known characters (whose reference images are included). The objective of this project is to (a) make bboyte's code more accessible and (b) illustrate, in a readable way, the fundamentals of captcha cracking. It's primary goal is clarity and makes no claims or attempts at efficiency, accuracy, or practicality.

This work is a derivation of an original work by @boyter
<bboyte01@gmail.com>, http://www.boyter.org/decoding-captchas/ (see
origin tutorial at
https://web.archive.org/web/20121012023114/http://www.wausita.com/captcha/)

## Installation

On ubuntu, libjpeg-dev and libpng-dev may be system requirements for the Python Pillow (PIL) library 

    sudo apt-get install libjpeg-dev
    sudo apt-get install libpng-dev
    
Next, fetch and build the decaptcha library

    pip install git+https://github.com/mekarpeles/captcha-decoder.git

## Usage

The decaptcha library comes with a command line utility called `decaptca`. Running the command with `-h` will show a list of options. The <img> argument can be provided a filepath or a url:

    usage: decaptcha [-h] [-v] [-l LIMIT] [-c CHANNELS] [-t THRESHOLD] [--min MIN]
                     [--max MAX] [-o TOLERANCE]
                     [<img>]
    
    Python captcha cracking utility
    
    positional arguments:
      <img>                 Enter the filesystem path or url of a captcha image
    
    optional arguments:
      -h, --help            show this help message and exit
      -v                    Displays the decaptcha version
      -l LIMIT, --limit LIMIT
                            Package url
      -c CHANNELS, --channels CHANNELS
                            The number of prominant color channels to keep
      -t THRESHOLD, --threshold THRESHOLD
                            Accuracy threshold for matching decimal [0-1]
      --min MIN             Filter out colors darker than this [0-256]
      --max MAX             Filter out colors light than this [0-256]
      -o TOLERANCE, --tolerance TOLERANCE
                            Pixel tolerance for character segmentation. Higher is
                            more lenient/greedy, lower is strict.

# Example

    $ decaptcha http://www.mondor.org/img/capex.jpg  --min 0 --max 20 --limit 5 --channels 5 --tolerance 7
    
    Character 0 of 7:
            t (confidence of 0.839150063096)
            e (confidence of 0.827405543276)
    Character 1 of 7:
            0 (confidence of 0.834057656228)
            l (confidence of 0.771064160322)
    Character 2 of 7:
            t (confidence of 0.309437274354)
            e (confidence of 0.303227199152)
    Character 3 of 7:
    Character 4 of 7:
            t (confidence of 0.267644230239)
            7 (confidence of 0.266067912114)
    Character 5 of 7:
            0 (confidence of 0.834057656228)
            l (confidence of 0.789422830806)
    Character 6 of 7:
            t (confidence of 0.835510535512)
            e (confidence of 0.835221298415)


## Further Reading

The following implementations and techniques are recommended as more practical and accurate alternatives for this project:

1. http://www.codeproject.com/Articles/106583/Handwriting-Recognition-Revisited-Kernel-Support-V
