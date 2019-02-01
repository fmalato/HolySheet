import binarizer as bin
import utils
import stringUtils
import os

import json
import cv2 as cv

bible = 'Muenchen'
binar = bin.Binarizer(bible)

with open('JsonUtils/groundTruthDictionary.json') as groundTruth:
    dictionary = json.load(groundTruth)

#with open('JsonUtils/angles.json') as aj:
 #   angles = json.load(aj)

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
        json.dump(inPagePositions, pp)"""



"""# utils.connectedComponents('testLine1.png')
for x in range(1, 7, 1):
    image = cv.imread('testLine{x}.png'.format(x=x))
    pts = binar.calimero(image)
    print(pts)"""

"""numImage = 1
for numPage in range(34, 62):
    numImage = utils.splitColumns('GenesisPages/old/MuenchenRotated/Gut-{x}.png'.format(x=numPage), numPage, numImage)

for file in os.listdir("test2019/"):
    os.rename("test2019/{file}".format(file=file), "test2019/{file}".format(file=file.zfill(9)))"""

"""id = 0
for x in range(14, 29, 1):
    if x % 2 == 0:
        cutWidthLeft = 450
        cutWidthRight = 450
    else:
        cutWidthLeft = 470
        cutWidthRight = 430
    id = utils.setAnnotations(nPage=x, cutWidthLeft=cutWidthLeft, cutHeight=250, id=id)"""

angs = {}
for x in range(34, 62):
    angle = binar.findRotationAngle('GenesisPages/old/Muenchen/Gut-0{x}.jpg'.format(x=x))
    angs[str(x)] = angle

with open('angles_34-62.json', 'w+') as f:
    json.dump(angs, f)

for x in range(34, 62):
    binar.rotateOriginals('GenesisPages/old/Muenchen/Gut-0{x}.jpg'.format(x=x), x, angs)

# Istruzioni: PRIMA ESEGUI LA PARTE NON COMMENTATA, cosi' da trovare gli angoli e ruotare le immagini (ci mette 2-3 min)
#             Dopo, scommenta da "numImage = 1" fino a "zfill(9)". il ciclo dopo si occupa delle annotations, ma per il
#             test non servono. Per il validation, aspetto i file caricati senza annotations, poi ci penso io! c:


