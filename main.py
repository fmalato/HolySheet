import binarizer as bin
import utils
import stringUtils

import json
import cv2 as cv

bible = 'Muenchen'
binar = bin.Binarizer(bible)

with open('JsonUtils/groundTruthDictionary.json') as groundTruth:
    dictionary = json.load(groundTruth)

with open('JsonUtils/angles.json') as aj:
    angles = json.load(aj)

# Variabile a True significa che e` possibile vedere le pagine singolarmente, altrimenti provvede a salvare le frequent
# words nella apposita cartella (richiede qualche minuto)
"""
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
                            None,
                            None
                            )


else:
    with open('JsonUtils/10mostFrequentWords.json') as fq:
        frequentWords = json.load(fq)

    # Dizionario delle posizioni assolute rispetto alla pagina di ciascuna parola, per creare successivamente le
    # annotazioni. La chiave piu` esterna rappresenta il numero di pagina che ha come valore un altro dizionario.
    # Quest`ultimo ha come chiavi le parole frequenti e come valore una lista di tuple. Ciascuna di esse rappresenta
    # la posizione all`interno della pagina. Es: "et": [(p1, p2, p3, p4), (p5, p6, p7, p8)...] (i punti sono presi
    # partendo dall`alto, da sinista a destra.

    inPagePositions = dict()

    for frequentWord in frequentWords:

        with open('JsonUtils/{frequentWord}Positions.json'.format(frequentWord=frequentWord)) as dfw:
            wordPositions = json.load(dfw)

        print()
        print(frequentWord)

        for numPage in range(14, 34):

            print("Page: " + str(numPage))

            if numPage not in inPagePositions.keys():
                inPagePositions[numPage] = dict()

            binar.linesCropping('GenesisPages/old/Muenchen/Gut-0{x}.jpg'.format(x=numPage),
                                numPage,
                                '_P{x}_C0'.format(x=(numPage - 14)),
                                '_P{x}_C1'.format(x=(numPage - 14)),
                                dictionary,
                                angles,
                                wordPositions,
                                frequentWord,
                                inPagePositions
                                )

    with open('inPagePositions.json', 'w') as pp:
        json.dump(inPagePositions, pp)



# utils.connectedComponents('testLine1.png')
for x in range(1, 7, 1):
    image = cv.imread('testLine{x}.png'.format(x=x))
    pts = binar.calimero(image)
    print(pts)"""

for numPage in range(14, 22):
    utils.splitColumns('GenesisPages/old/MuenchenRotated/Gut-{x}.png'.format(x=numPage), numPage)

