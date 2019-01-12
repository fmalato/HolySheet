import binarizer as bin
import utils

import json
import cv2 as cv
import numpy as np

bible = 'Muenchen'
binar = bin.Binarizer(bible)

# binar.binarize()

"""img = cv.imread('threshed.jpg')
cropped = cv.imread('cropped.png')
cropped2 = cv.imread('cropped4.png')
#pts = binar.calimero(img, cropped)
pts = binar.two_way_calimero(img, cropped, cropped2)
print(pts)"""

with open('groundTruthDictionary.json') as groundTruth:
    dictionary = json.load(groundTruth)

# Problemi patologici su pag14, cattiva segmentazione su pag31

with open('angles.json') as aj:
    angles = json.load(aj)

#for numPage in range(14, 34):

"""numPage = 18

binar.linesCropping('GenesisPages/old/Muenchen/Gut-0{x}.jpg'.format(x=numPage),
                    numPage,
                    '_P{x}_C0'.format(x=(numPage - 14)),
                    '_P{x}_C1'.format(x=(numPage - 14)),
                    dictionary,
                    angles)"""

img = cv.imread('thresh.png')
utils.hola(img)

