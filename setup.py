# -*- coding: utf-8 -*-

"""
    decaptcha
    ~~~~~~~~~

"""

import codecs
import os
import re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Taken from pypa pip setup.py:
    intentionally *not* adding an encoding option to open, See:
    https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    """
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='decaptcha',
    version=find_version("decaptcha", "__init__.py"),
    description='Python captcha cracking utility',
    long_description=read('README.md'),
    url='http://github.com/mekarpeles/captcha-decoder',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'decaptcha',
        ],
    platforms='any',
    license='LICENSE',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
        ],
    install_requires=[
        'Pillow >= 2.9.0'
        ],
    entry_points={
        'console_scripts': ['decaptcha=decaptcha.cli:main'],
        },
    extras_require={
        ':python_version=="2.7"': ['argparse']
        },
    include_package_data=True,
    package_data={'': ['iconset/**/*.gif']},
)
