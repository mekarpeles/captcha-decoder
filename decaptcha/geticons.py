#-*- coding: utf-8 -*-

"""
    geticons.py
    ~~~~~~~~~

    This module takes captcha images, preprocesses them (saving the
    processed intermediary captcha as output_<timestamp>.gif),
    determines where all the characters are within the image, and then
    partitions the preprocessed captcha image into n new images, 1
    image per character found.

    Originally written by bboyte01@gmail.com, http://www.wausita.com/captcha/

    :copyright: (c) 2012 by Mek
    :license: Creative Commons, see LICENSE for more details.
"""

from PIL import Image
from datetime import datetime
import hashlib
import time
import sys

def format_image(im)
  timestamp = datetime.now().isoformat().split(":")[-1]
  im2 = Image.new("P",im.size,255)
  im1 = im.convert("P")
  
  temp = {}
  for x in range(im1.size[1]):
    for y in range(im1.size[0]):
      pix = im1.getpixel((y,x))
      temp[pix] = pix
      if pix == 220 or pix == 227: # these are the numbers to get
        im2.putpixel((y,x),0)    
  im2.save("output_%s.gif" % timestamp)
  return im2

def find_letters(im2):
  inletter = False
  foundletter=False
  start = 0
  end = 0
  
  letters = []

  for y in range(im2.size[0]): # slice across (y axis)
    for x in range(im2.size[1]): # slice down
      pix = im2.getpixel((y,x))
      if pix != 255:
        inletter = True

    if not foundletter and inletter:
      foundletter = True
      start = y

    if foundletter and not:
      foundletter = False
      end = y
      letters.append((start,end))
    inletter=False
  return letters

def save_letters(im2, letters):
  """
  """
  count = 0
  for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    m.update("%s%s"%(time.time(),count))
    im3.save("./%s.gif"%(m.hexdigest()))
    count += 1

def segment(captcha):
  """Partitions the origin image into segments, each containing
  (hopefully) a single character.
  """
  im = Image.open(captcha)
  im2 = open_image(im)
  

#if __name__ == "__main__":
try:
  captcha = sys.argv[1]
except:
  captcha = "captcha.gif"
segment(captcha)
