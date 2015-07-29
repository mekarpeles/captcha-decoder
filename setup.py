# -*- coding: utf-8 -*-

"""
    decaptcha
    ~~~~~~~~~

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

setup(
    name='decaptcha',
    version='0.0.1',
    url='http://github.com/mekarpeles/captcha-decoder',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'decaptcha',
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
    ],
    scripts=[
        'scripts/decaptcha'
        ],
    description='Basic Captcha Cracker',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    include_package_data=True
)
