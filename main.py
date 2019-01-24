import binarizer as bin

import json
import cv2 as cv

bible = 'Muenchen'
binar = bin.Binarizer(bible)

image = cv.imread('testLine1.png')
#"""
# binar.binarize()

with open('JsonUtils/groundTruthDictionary.json') as groundTruth:
    dictionary = json.load(groundTruth)

with open('JsonUtils/angles.json') as aj:
    angles = json.load(aj)

# Variabile a True significa che e` possibile vedere le pagine singolarmente, altrimenti provvede a salvare le frequent
# words nella apposita cartella (richiede qualche minuto)

inspector = False

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

    for frequentWord in frequentWords:

        with open('JsonUtils/{frequentWord}Positions.json'.format(frequentWord=frequentWord)) as dfw:
            wordPositions = json.load(dfw)

        print()
        print(frequentWord)

        for numPage in range(14, 34):

            print("Page: " + str(numPage))

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
    pts = binar.calimero(image)
    print(pts)"""