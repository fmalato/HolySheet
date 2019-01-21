import binarizer as bin
import utils
import stringUtils

import json
import cv2 as cv
import numpy as np

bible = 'Muenchen'
binar = bin.Binarizer(bible)

image = cv.imread('testLine1.png')

# binar.binarize()

with open('JsonUtils/groundTruthDictionary.json') as groundTruth:
    dictionary = json.load(groundTruth)

with open('JsonUtils/angles.json') as aj:
    angles = json.load(aj)

# Variabile a True significa che e` possibile vedere le pagine singolarmente, altrimenti provvede a salvare le frequent
# words nella apposita cartella (richiede qualche minuto)

inspector = True

if inspector:

    for numPage in range(15, 21):
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

    numPage = 18
    frequentWord: object
    for frequentWord in frequentWords:

        with open('JsonUtils/{frequentWord}Positions.json'.format(frequentWord=frequentWord)) as dfw:
            wordPositions = json.load(dfw)

        for numPage in range(15, 21):

            binar.linesCropping('GenesisPages/old/Muenchen/Gut-0{x}.jpg'.format(x=numPage),
                                numPage,
                                '_P{x}_C0'.format(x=(numPage - 14)),
                                '_P{x}_C1'.format(x=(numPage - 14)),
                                dictionary,
                                angles,
                                wordPositions,
                                frequentWord
                                )

# utils.connectedComponents('testLine1.png')
"""for x in range(1, 7, 1):
    image = cv.imread('testLine{x}.png'.format(x=x))
    pts = binar.true_calimero(image)
    for pt in pts:
        cv.rectangle(image, (pt[1] - 2, pt[0]), (pt[1] + 5, pt[0] + 5), (0, 0, 255), 1)
    cv.imwrite('calimero_test/points{x}.png'.format(x=x), image)

    print(pts)"""