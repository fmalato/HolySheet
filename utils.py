import cv2 as cv
import json
#import pytesseract
import numpy as np
import collections
import binarizer as binar
import os

from PIL import Image

def findCentroids(img):

    # convert image to grayscale image
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # convert the grayscale image to binary image
    ret, thresh = cv.threshold(gray_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)

    cv.imwrite('thresh.png', thresh)

    # calculate moments of binary image
    M = cv.moments(thresh)

    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # put text and highlight the center
    cv.circle(img, (cX, cY), 5, (255, 0, 0), -1)
    cv.putText(img, "centroid", (cX - 25, cY - 25), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv.imshow('centroids', img)
    cv.waitKey(0)


def connectedComponents(image):

    height, width = image.shape[0], image.shape[1]

    start_row, start_col = int(height*0.5), int(0)
    # Taglia l'immagine a meta`, per eliminare un certo numero di variabili che, computazionalmente, pesano.
    end_row, end_col = int(height), int(width)
    croppedImage = image[start_row:end_row , start_col:end_col]

    gray = cv.cvtColor(croppedImage, cv.COLOR_BGR2GRAY)
    _, threshed = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)    # BINARY non INV se gli si passa black n white

    height, width = croppedImage.shape[0], croppedImage.shape[1]

    numComponent = 1

    # La prima riga composta da zeri sta qui per evitare errori sugli indici, piu` avanti viene eliminata
    components = [[0 for x in range(width)]]
    conflicts = {}

    # Questo tripudio di logica booleana e` praticamente l'algoritmo che mappa i pixel != 0 con valori != 0

    for row in range(height):
        line = []
        for col in range(width):
            if threshed[row][col] == 0:
                line.append(0)
            elif threshed[row][col] == 255:
                if threshed[row][col - 1] == 255 or threshed[row - 1][col] == 255:
                    if col > 0:
                        if components[row][col] == line[col - 1]:
                            line.append(line[col - 1])
                        elif components[row][col] != line[col - 1]:
                            if components[row][col] != 0 and line[col - 1] != 0:
                                if line[col - 1] not in conflicts.keys():
                                    conflicts[line[col - 1]] = []
                                conflicts[line[col - 1]].append(components[row][col])
                                line.append(line[col - 1])
                            else:
                                if threshed[row][col - 1] == 0:
                                    line.append(components[row][col])
                                else:
                                    line.append(line[col - 1])
                    else:
                        if threshed[row - 1][col] == 255:
                            line.append(components[row][col])
                        else:
                            line.append(numComponent)

                elif threshed[row][col - 1] == 0 and threshed[row - 1][col] == 0:
                    numComponent += 1
                    line.append(numComponent)
        components.append(line)

    # Rimuovo per evitare una riga nera all'inizio di ogni immagine (meno variabili)
    components.pop(0)

    # Eh, questi tre blocchi di cicli sono... sostanzialmente sotterfugi per riordinare come si deve i conflitti.
    for key in conflicts.keys():
        conflicts[key] = list(set(conflicts[key]))

    newKeys = []
    for key in conflicts.keys():
        while len(conflicts[key]) > 1:
            newKeys.append((key, conflicts[key][0]))
            conflicts[key].pop(0)

    for el in newKeys:
        if el[1] not in conflicts.keys():
            conflicts[el[1]] = []
        conflicts[el[1]].append(el[0])
        if len(conflicts[el[1]]) > 1 and ((el[0], conflicts[el[1]][0]) not in newKeys):
            newKeys.append((el[0], conflicts[el[1]][0]))
            conflicts[el[1]].pop(0)

    # Riordina il dizionario dei conflitti e li risolve con i cicli for seguenti. Purtroppo non ho modo di farlo piu`
    # rapidamente (se ti viene in mente un modo, ben venga)!

    conflicts = sortDict(conflicts)

    for key in list(conflicts.keys())[::-1]:
        for row in range(height):
            for col in range(width):
                if key == components[row][col]:
                    components[row][col] = conflicts[key][0]
        for k in conflicts.keys():
            if conflicts[k] == [key]:
                conflicts[k] = [conflicts[key][0]]

    # json mi serviva solo per visualizzare le componenti in fase di test
    # with open('comp.json', 'w+') as f:
        # json.dump(components, f)

    # Serve per mantenere solo le componenti connesse composte da al massimo un certo numero di pixel. Purtroppo anche
    # questo e` cubico. Sul mio fisso pero` funziona bene, se usiamo soltanto la riga.
    numPixels = {}
    for row in components:
        for col in row:
            if col != 0:
                if col not in numPixels.keys():
                    numPixels[col] = 1
                else:
                    numPixels[col] += 1

    blacks = []
    for key in numPixels.keys():
        if numPixels[key] >= 20 or numPixels[key] <= 5:
            for row in range(height):
                for col in range(width):
                    if components[row][col] == key:
                        components[row][col] = 0
        else:
            blacks.append(key)

    # Questi ultimi cicli si occupano di restituire le coordinate di ciascuna componente connessa rimasta
    found = []
    coords = {}
    for row in range(height):
        for col in range(width):
            if components[row][col] != 0 and components[row][col] not in found:
                found.append(components[row][col])
                coords[components[row][col]] = (row + start_row, col)    # ATTENZIONE: in coordinate cartesiane sono (y, x)

    # Da qui in poi viene generata l'immagine nuova, lo elimino dopo aver fatto qualche test sula pagina effettiva
    """image = []
    for comp in components:
        imgLine = []
        for el in comp:
            if el != 0:
                imgLine.append((255, 255, 255))
            else:
                imgLine.append((0, 0, 0))
        image.append(imgLine)

    imgArray = np.array(image, dtype=np.uint8)
    #img = Image.fromarray(imgArray)
    cv.imwrite('generated.png', imgArray)
    img = cv.imread('generated.png')
    for key in coords.keys():
        cv.rectangle(img, (coords[key][1], coords[key][0] - start_row), 
                     (coords[key][1] + 5, height - coords[key][0] - start_row), (0, 0, 255), 1)
    cv.imwrite('generated.png', img)"""

    return [coords[key] for key in coords.keys()]


def sortDict(dictionary):

    keysList = [key for key in dictionary.keys()]
    keysList.sort()

    newDict = collections.OrderedDict()

    for key in keysList:
        newDict[key] = dictionary[key]

    return newDict

def splitColumns(image_path, nPage):

    # La mia indecisione sta nel fatto che forse è più comodo salvarsi le dimensioni delle colonne in un .json,
    # effettuare il taglio  usando l'immagine intera e poi salvare i risultati tipo in una cartella "dataset"

    img = cv.imread(image_path)

    numCuts = 5

    with open('instances_COCOGenesis.json') as instances:
        COCOGenesis = json.load(instances)

    with open('inPagePositions.json') as pp:
        pagePositions = json.load(pp)

    # TODO inserire ogni immagine tagliata in COCOGenesis["images"] compilando i relativi campi (append.({roba...})

    imageHeight = 1250
    imageWidth = 900
    cutHeight = int(imageHeight/numCuts)
    cutWidth = int(imageWidth/2)
    if nPage % 2 is not 0:
        cutWidth = int(imageWidth/2 + 20)

    if not os.path.exists('trainImages/'.format(nPage=nPage)):
        os.mkdir('trainImages')
    if not os.path.exists('trainImages/images_{nPage}'.format(nPage=nPage)):
        os.mkdir('trainImages/images_{nPage}'.format(nPage=nPage))

    # TODO leggere dal file PagePositions le posizioni ci ciascuna parola e provare ad inserirle: idea stupida potrebbe
    #  essere quella di vedere se ci sta con un try except (se effettivamente appartiene tutta all'immaginetta
    #  tagliata, altrimenti continue. Salvare le annotazioni nel COCOGenesis

    for i in range(numCuts):
        cropped = img[i*cutHeight:(i+1)*cutHeight, 0:cutWidth]
        cv.imwrite('trainImages/images_{nPage}/0000{x}.png'.format(nPage=nPage, x=i), cropped)
    for i in range(numCuts):
        cropped = img[i*cutHeight:(i+1)*cutHeight, cutWidth:imageWidth]
        cv.imwrite('trainImages/images_{nPage}/0000{x}.png'.format(nPage=nPage, x=i+numCuts), cropped)


    # TODO ricordarsi di risalvare il json delle annotazioni :)


