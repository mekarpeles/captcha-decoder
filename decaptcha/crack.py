#-*- coding: utf-8 -*-

"""
    crack.py
    ~~~~~~~~

    This module takes captcha images as input and partitions them into
    n new images, 1 image per character found within the captcha.

    Originally written by bboyte01@gmail.com, http://www.wausita.com/captcha/

    :copyright: (c) 2012 by Abel and Mek
    :license: Creative Commons, see LICENSE for more details.
"""

import hashlib
import time
import os
import math
import string
from PIL import Image
from datetime import datetime
from util import build_imgset

IMAGESET = build_imageset()

def magnitude(self, concordance):
  """
  """
  total = 0
  for word,count in concordance.iteritems():
    total += count ** 2
  return math.sqrt(total)

def relation(self, concordance1, concordance2):
  """
  """
  relevance = 0
  topvalue = 0
  for word, count in concordance1.iteritems():
    if concordance2.has_key(word):
      topvalue += count * concordance2[word]
  return topvalue / (magnitude(concordance1) * magnitude(concordance2))



def crack_captcha(captcha):
  """currently only works with gifs"""  
  im2 = preprocess_captcha(captcha)
  characters = find_characters(im2)
  save_characters(im2, captcha, characters)

def preprocess_captcha(captcha):
  """
  """
  im = Image.open("captcha.gif")
  im1 = im.convert("P")
  im2 = Image.new("P", im.size,255)

  temp = {}
  for x in range(im1.size[1]):
    for y in range(im1.size[0]):
      pix = im1.getpixel((y,x))
      temp[pix] = pix
      if pix < 10: # these are the numbers to get
        im2.putpixel((y,x),0)
  im2.save("output.gif")
  return im2

def find_characters(im2):
  """Split up the preprocessed captcha to find individual characters
  and accumulate a list of its start and end coordinates
  """
  letters = []
  inletter = False
  foundletter = False
  start = 0
  end = 0

  for y in range(im2.size[0]): # slice across
    for x in range(im2.size[1]): # slice down
      pix = im2.getpixel((y,x))
      if pix != 255:
        inletter = True

    if not foundletter and inletter:
      foundletter = True
      start = y

    if foundletter and not inletter:
      foundletter = False
      end = y
      letters.append((start,end))

    inletter=False
  return letters

def save_characters(im2, captcha, letters):
  """
  """
  count = 0
  for letter in letters:
    guess = []
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    im3_filename = "./output/%s-%s_%s.gif" % (captcha, count, int(time.time()))
    im3.save(im3_filename)
    count += 1

    for character in IMAGESET:
      for x,y in character.iteritems():
        if len(y) != 0:
          guess.append((relation(y[0], buildvector(im3)), x))
          
    guess.sort(reverse=True)
    print "", guess[0]
    count += 1

#if __name__ == "__main__":
try:
  captcha = sys.argv[1]
except:
  captcha = "captcha.gif"
crack_captcha(captcha)
