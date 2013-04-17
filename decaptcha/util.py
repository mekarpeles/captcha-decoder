import os
import string
from PIL import Image

SYMBOLS = list(string.digits + string.lowercase)
APP_PATH = os.path.dirname(__file__)

def buildvector(im):
  d1 = {}
  for count, i in enumerate(im.getdata()):
    d1[count] = i
  return d1

def crop_white(img):
  min_coord = img.size[1]+10
  max_coord = -1
  for y in range(img.size[0]): # slice across
    for x in range(img.size[1]): # slice down
    	pix = img.getpixel((y,x))
    	if pix != 255:
    		min_coord = min(min_coord,x)
    		max_coord = max(max_coord,x)
  return img.crop((0, min_coord, img.size[0], max_coord))

def build_imgset():
    imageset = []
    for letter in SYMBOLS:
      for img in os.listdir('%s/iconset/%s/' % (APP_PATH, letter)):
        temp = []
        if img != "Thumbs.db": # windows check...
          im = Image.open("%s/iconset/%s/%s" % (APP_PATH, letter, img))
          temp.append(im)       
        imageset.append({letter:temp})
    return imageset
