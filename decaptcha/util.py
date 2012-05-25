import os
import string
from PIL import Image

ICONSET = list(string.lowercase + string.digits)

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
    for count, character in enumerate(ICONSET):
        for img in os.listdir('./iconset/%s/' % (character)):
            temp = []
            if img != "Thumbs.db": # windows check...
                im = Image.open("./iconset/%s/%s" % (character, img))
                im = crop_white(im)
                im.save("output-%s.gif" % (count))
                im.save("./iconset/%s/%s" % (character, img))
                temp.append(buildvector(im))
            imageset.append({character: temp})
    return imageset
