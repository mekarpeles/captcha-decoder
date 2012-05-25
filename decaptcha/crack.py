#-*- coding: utf-8 -*-

"""
    crack.py
    ~~~~~~~~

    This module takes captcha images as input and partitions them into
    n new images, 1 image per character found within the captcha.

    Original by bboyte01@gmail.com, http://www.wausita.com/captcha/

    :copyright: (c) 2012 by Abel and Mek
    :license: Creative Commons, see LICENSE for more details.
"""

import hashlib
import time
import math
import string
from PIL import Image
from datetime import datetime
from util import build_imgset, buildvector, crop_white

IMAGESET = build_imgset()

def magnitude(concordance):
  """
  """
  total = 0
  for word,count in concordance.iteritems():
    total += count ** 2
  return math.sqrt(total)

def relation(concordance1, concordance2):
  """
  """
  relevance = 0
  for word, count in concordance1.iteritems():
    if concordance2.has_key(word) and count == concordance2[word]:
      if count == 0:
        relevance += 5
      else:
        relevance += 1
  return float(relevance)/float(len(concordance2))

def preprocess_captcha(captcha):
  """
  """
  im = Image.open(captcha).convert("P")
  im2 = Image.new("P", im.size,255)
  temp = {}
  for x in range(im.size[1]):
    for y in range(im.size[0]):
      pix = im.getpixel((y,x))
      temp[pix] = pix
      if pix < 10: # these are the numbers to get
        im2.putpixel((y,x),0)
  im2.save("./output/output.gif")
  return im2

def find_characters(im):
  """Split up the preprocessed captcha to find individual characters
  and accumulate a list of its start and end coordinates
  """
  letters = []
  inletter = False
  foundletter = False
  start = 0
  end = 0

  for y in range(im.size[0]): # slice across
    for x in range(im.size[1]): # slice down
      pix = im.getpixel((y,x))
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

def segment_characters(im, characters):
  """Iterates over all discrete segments containing characters found
  within the captcha, crops them and saved them as individual icons
  """
  segments = []
  for count, character in enumerate(characters):
    segment_filename = "./output/%s_%s.gif" % (int(time.time()), count)
    segment = crop_white(im.crop((character[0], 0,
                                  character[1], im.size[1])))
    segment.save(segment_filename)
    segments.append(segment)
  return segments

def guess_characters(segments):
  """Loops over each segment and attempts to guess what character is
  contained within the cropped img
  """
  for segment in segments:
    guess = []
    for icon in IMAGESET:
      for x,y in icon.iteritems():
        if len(y):
          for option in y:
            im4 = segment.resize(option.size)
            guess.append((relation(buildvector(option),
                                   buildvector(im4)),x))
    guess.sort(reverse=True)
    print "", guess[0]

def crack_captcha(captcha):
  """driver/entry point for crack.py
  currently only works with gifs
  """    
  im = preprocess_captcha(captcha)
  chars = find_characters(im)
  segments = segment_characters(im, chars)
  guess_characters(segments)

if __name__ == "__main__":
  try:
    captcha = sys.argv[1]
  except:
    captcha = "captcha.gif"
  crack_captcha(captcha)
