import binarizer as bin
import utils
import stringUtils

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

with open('JsonUtils/groundTruthDictionary.json') as groundTruth:
    dictionary = json.load(groundTruth)

with open('JsonUtils/angles.json') as aj:
    angles = json.load(aj)

# Variabile a True significa che e` possibile vedere le pagine singolarmente, altrimenti provvede a salvare le frequent
# words nella apposita cartella (richiede qualche minuto)

inspector = True

if inspector:

    for numPage in range(14, 21):
        binar.linesCropping('GenesisPages/old/Muenchen/Gut-0{x}.jpg'.format(x=numPage),
                            numPage,
                            '_P{x}_C0'.format(x=(numPage - 14)),
                            '_P{x}_C1'.format(x=(numPage - 14)),
                            dictionary,
                            angles,
                            None,
                            None
                            )


else:
    with open('JsonUtils/10mostFrequentWords.json') as fq:
        frequentWords = json.load(fq)

"""numPage = 18
    frequentWord: object
    for frequentWord in frequentWords:

        with open('JsonUtils/{frequentWord}Positions.json'.format(frequentWord=frequentWord)) as dfw:
            wordPositions = json.load(dfw)

        for numPage in range(14, 21):

            binar.linesCropping('GenesisPages/old/Muenchen/Gut-0{x}.jpg'.format(x=numPage),
                                numPage,
                                '_P{x}_C0'.format(x=(numPage - 14)),
                                '_P{x}_C1'.format(x=(numPage - 14)),
                                dictionary,
                                angles,
                                wordPositions,
                                frequentWord
                                )"""

# img = cv.imread('thresh.png')
# utils.hola(img)

