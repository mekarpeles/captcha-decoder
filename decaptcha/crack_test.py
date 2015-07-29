import hashlib
import os
import math

from PIL import Image

from util import SYMBOLS


class VectorCompare(object):

    @classmethod
    def magnitude(cls, concordance):
        total = 0
        for word, count in concordance.iteritems():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.iteritems():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


def buildvector(img):
    d1 = {}

    count = 0
    for i in img.getdata():
        d1[count] = i
        count += 1

    return d1

v = VectorCompare()

imageset = []

for letter in SYMBOLS:
    for im in os.listdir('./iconset/%s/' % letter):
        temp = []
        if im != 'Thumbs.db':  # windows check...
            temp.append(buildvector(Image.open('./iconset/%s/%s' % (letter, im))))
        imageset.append({letter: temp})

correctcount = 0
wrongcount = 0


for filename in os.listdir('../examples/'):
    try:
        im = Image.open('../examples/%s' % filename)
    except:
        break

    print ''
    print filename

    im2 = Image.new('P', im.size, 255)
    im = im.convert('P')
    temp = {}

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            temp[pix] = pix
            if pix == 220 or pix == 227:  # these are the numbers to get
                im2.putpixel((y, x), 0)

    inletter = False
    foundletter = False
    start = 0
    end = 0

    letters = []

    for y in range(im2.size[0]):  # slice across
        for x in range(im2.size[1]):  # slice down
            pix = im2.getpixel((y, x))
            if pix != 255:
                inletter = True

        if foundletter is False and inletter is True:
            foundletter = True
            start = y

        if foundletter is True and inletter is False:
            foundletter = False
            end = y
            letters.append((start, end))

        inletter = False

    guessword = ''
    for letter in letters:
        m = hashlib.md5()
        im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))

        guess = []

        for image in imageset:
            for x, y in image.iteritems():
                if len(y) != 0:
                    guess.append((v.relation(y[0], buildvector(im3)), x))

        guess.sort(reverse=True)
        print '', guess[0]
        guessword = '%s%s' % (guessword, guess[0][1])

    if guessword == filename[:-4]:
        correctcount += 1
    else:
        wrongcount += 1


print '======================='
correctcount = float(correctcount)
wrongcount = float(wrongcount)
print 'Correct Guesses - ', correctcount
print 'Wrong Guesses - ', wrongcount
print 'Percentage Correct - ', correctcount / (correctcount + wrongcount) * 100.00
print 'Percentage Wrong - ', wrongcount / (correctcount + wrongcount) * 100.00
