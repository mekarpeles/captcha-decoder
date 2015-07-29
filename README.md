captcha-decoder
===============

![Build Status](https://travis-ci.org/mekarpeles/captcha-decoder.png)

This module takes a captcha (image) as input and partitions it into
what it believes are n new images, where each new image is a discrete
character found within the original captcha.

This work is a derivation of an original work by @boyter <bboyte01@gmail.com>,
http://www.boyter.org/decoding-captchas/.

## Example

    $ decaptcha captcha.jpg 
    captcha.jpg
    (1.8571428571428572, 'f')
    (1.375, 'e')
    (1.43, 'u')
    (1.4, 'h')
    (1.52, 'u')
    (1.5125, 'e')

## License 

Creative Commons

## Further Reading

The objective of this project was to (a) make bboyte's code more
accessible and (b) demonstrate the fundamentals of captcha cracking.

The following implementations and techniques are recommended 
as more practical and accurate alternatives for this project:

1. http://www.codeproject.com/Articles/106583/Handwriting-Recognition-Revisited-Kernel-Support-V
