
from PIL import Image
import hashlib
import time
import os


import math


def crop_white(img):
  min_coord = img.size[1]+10
  max_coord = -1
  for y in range(img.size[0]): # slice across
    for x in range(img.size[1]): # slice down
    	pix = img.getpixel((y,x))
    	if pix != 255:
    		min_coord = min(min_coord,x)
    		max_coord = max(max_coord,x)

  img = img.crop(( 0, min_coord, img.size[0], max_coord))
  return img

class VectorCompare:

  def relation(self,concordance1, concordance2):
    relevance = 0
    for word, count in concordance1.iteritems():
      if concordance2.has_key(word) and count == concordance2[word]:
	if count == 0:
           relevance += 5
	else:
	   relevance += 1
    return float(relevance)/float(len(concordance2))


def buildvector(im):
  d1 = {}

  count = 0
  for i in im.getdata():
    d1[count] = i
    count += 1

  return d1

v = VectorCompare()


iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


imageset = []

for letter in iconset:
  for img in os.listdir('./iconset/%s/'%(letter)):
    temp = []
    if img != "Thumbs.db": # windows check...
	im = Image.open("./iconset/%s/%s"%(letter,img))
	temp.append(im)       
    imageset.append({letter:temp})


im = Image.open("captcha.gif")
im2 = Image.new("P",im.size,255)
im = im.convert("P")
temp = {}

for x in range(im.size[1]):
  for y in range(im.size[0]):
    pix = im.getpixel((y,x))
    temp[pix] = pix
    if pix < 10: # these are the numbers to get
      im2.putpixel((y,x),0)

im2.save("output.gif")

    
inletter = False
foundletter=False
start = 0
end = 0

letters = []

for y in range(im2.size[0]): # slice across
  for x in range(im2.size[1]): # slice down
    pix = im2.getpixel((y,x))
    if pix != 255:
      inletter = True

  if foundletter == False and inletter == True:
    foundletter = True
    start = y

  if foundletter == True and inletter == False:
    foundletter = False
    end = y
    letters.append((start,end))


  inletter=False

count = 0
for letter in letters:
  m = hashlib.md5()
  im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))

  im3 = crop_white(im3)

  m.update("%s%s"%(time.time(),count))
  im3.save("./%s--%s.gif"%(count,m.hexdigest()))
  count += 1

  guess = []

  for image in imageset:
    for x,y in image.iteritems():
      if len(y) != 0:
	for option in y:
		im4 = im3.resize(option.size)
        	guess.append( ( v.relation(buildvector(option),buildvector(im4)),x) )

  guess.sort(reverse=True)
  print guess[0],""
  count += 1

