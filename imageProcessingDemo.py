import binarizer as bin
import os

import json
import cv2 as cv

bible = 'Muenchen'
binar = bin.Binarizer(bible)

"""#with open('JsonUtils/groundTruthDictionary.json') as groundTruth:
    dictionary = json.load(groundTruth)

with open('JsonUtils/angles.json') as aj:
    angles = json.load(aj)

# Variabile a True significa che e` possibile vedere le pagine singolarmente, altrimenti provvede a salvare le frequent
# words nella apposita cartella (richiede qualche minuto)

inspector = False

if inspector:

    for numPage in range(24, 34):
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
    with open('JsonUtils/20mostFrequentWords.json') as fq:
        frequentWords = json.load(fq)

    # inPagePositions: Dizionario delle posizioni assolute rispetto alla pagina di ciascuna parola, per creare
    # successivamente le annotazioni. La chiave piu` esterna rappresenta il numero di pagina che ha come valore un altro
    # dizionario.
    # Quest`ultimo ha come chiavi le parole frequenti e come valore una lista di tuple. Ciascuna di esse rappresenta
    # la posizione all`interno della pagina. Es: "et": [(xTopLeft, yTopLeft, width, height), ...]
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
        json.dump(inPagePositions, pp)"""

