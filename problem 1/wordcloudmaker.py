import nltk
# import re, pprint, os, sys
from nltk import word_tokenize
from nltk.corpus import stopwords
import random
import array
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import numpy as np
#from query_integral_image import query_integral_image


def query_integral_image(integral_image, size_x, size_y):
    x = integral_image.shape[0]
    y = integral_image.shape[1]
    hits = 0

    # count how many possible locations
    for i in range(x - size_x):
        for j in range(y - size_y):
            area = integral_image[i, j] + integral_image[i + size_x, j + size_y]
            area -= integral_image[i + size_x, j] + integral_image[i, j + size_y]
            if not area:
                hits += 1
    if not hits:
        # no room left
        return None
    # pick a location at random
    goal = np.random.randint(hits)
    hits = 0
    for i in range(x - size_x):
        for j in range(y - size_y):
            area = integral_image[i, j] + integral_image[i + size_x, j + size_y]
            area -= integral_image[i + size_x, j] + integral_image[i, j + size_y]
            if not area:
                hits += 1
                if hits == goal:
                    return i, j



FONT_PATH = "C:\Windows\Fonts\BASKVILL.TTF"


tokens = word_tokenize(open("reddit2.txt").read())
#outfile = open("freqdist.txt", mode='w')
#orig_stdout = sys.stdout
#sys.stdout = outfile
tokenlist = []

redditstopwords = ['permalinkembed', 'save', 'gold', 'reply', 'parent', 'days', 'hours', 'permalink', 'embed', 'parent', 'give', 'report', 'reddit', 'points', 'ago']

for word in tokens: 
    word = word.lower() 
    if word.isalpha():
        tokenlist.append(word) 

filtered_tokens = [word for word in tokenlist if word not in stopwords.words('english') and word not in redditstopwords]

wor = []
counts = []

fdist1 = nltk.FreqDist(filtered_tokens)

#fdist1.sort(reverse=True)
for (token, freq) in fdist1.most_common(100):
    if freq<100 and freq>5:
        wor.append(token)
        ct = float(freq)/100
        counts.append(ct)
       # print (token, ':', fdist1[token])

fname = 'cloud.png'

width = 400
height = 200
font_path=FONT_PATH
margin=5 
ranks_only=False
prefer_horiz=0.9

# create image
img_grey = Image.new("L", (width, height))
draw = ImageDraw.Draw(img_grey)
integral = np.zeros((height, width), dtype=np.uint32)
img_array = np.asarray(img_grey)
font_sizes, positions, orientations = [], [], []
# intitiallize font size "large enough"
font_size = 1000
# start drawing grey image
for word, count in zip(wor, counts):
    # alternative way to set the font size
    if not ranks_only:
        font_size = min(font_size, int(100 * np.log(count + 100)))
    while True:
        try:
            # try to find a position
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            fontfile = FONT_PATH.rsplit('/', 1)[-1]
            raise IOError("Font '%s' not found. Please change 'FONT_PATH' "
                          "to a valid font file path." % fontfile)
        # transpose font optionally
        if random.random() < prefer_horiz:
            orientation = None
        else:
            orientation = Image.ROTATE_90
        transposed_font = ImageFont.TransposedFont(font, orientation=orientation)
        draw.setfont(transposed_font)
        # get size of resulting text
        box_size = draw.textsize(word)
        # find possible places using integral image:
        result = query_integral_image(integral, box_size[1] + margin,
                                      box_size[0] + margin)
        if result is not None or font_size == 0:
            break
        # if we didn't find a place, make font smaller
        font_size -= 1

    if font_size == 0:
        # we were unable to draw any more
        break

    x, y = np.array(result) + margin // 2
    # actually draw the text
    draw.text((y, x), word, fill="white")
    positions.append((x, y))
    orientations.append(orientation)
    font_sizes.append(font_size)
    # recompute integral image
    img_array = np.asarray(img_grey)
    # recompute bottom right
    # the order of the cumsum's is important for speed ?!
    partial_integral = np.cumsum(np.cumsum(img_array[x:, y:], axis=1),
                                 axis=0)
    # paste recomputed part into old image
    # if x or y is zero it is a bit annoying
    if x > 0:
        if y > 0:
            partial_integral += (integral[x - 1, y:]
                                 - integral[x - 1, y - 1])
        else:
            partial_integral += integral[x - 1, y:]
    if y > 0:
        partial_integral += integral[x:, y - 1][:, np.newaxis]

    integral[x:, y:] = partial_integral

img_grey.show()
img_grey.save(fname)






#sys.stdout = orig_stdout
#outfile.close()
