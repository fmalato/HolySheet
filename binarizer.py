import cv2 as cv
import os
#import imutils
import numpy as np
import math
import scipy

from scipy import ndimage
from matplotlib import pyplot as plt
from PIL import Image

# Le immagini vengono salvate nel path specificato da save_path e caricate dal path specificato in
# read_path, che si basano entrambi sul nome del documento (bible). Agisci solo su queste variabili
# per modificare i percorsi, il programma pensa al resto.


class Binarizer:

    def __init__(self, bible):
        self.bible = bible
        self.read_path = 'GenesisPages/old/{bible}'.format(bible=self.bible)
        self.save_path = 'GenesisPages/old/{bible}_binarized'.format(bible=self.bible)

    def set_bible(self, bible):
        self.bible = bible
        self.read_path = 'GenesisPages/old/{bible}'.format(bible=self.bible)
        self.save_path = 'GenesisPages/old/{bible}_binarized'.format(bible=self.bible)

    # TODO: decidere come comportarsi con le miniate e i caput, che cambiano colore e risultano difficili da binarizzare.

    def binarize(self):

        # Se le cartelle per salvare le immagini non esistono, vengono create, altrimenti viene riutilizzata
        # quella gia' presente.

        if not os.path.exists(self.save_path):
            os.mkdir('{save_path}/'.format(save_path=self.save_path))
            print('Directory created.')
        else:
            print('Directory found.')

        for image in os.listdir('GenesisPages/old/{doc}/'.format(doc=self.bible)):

            # Rimuove il formato dalla stringa che identifica il nome dell'immagine (almeno dopo posso cambiare
            # da .jpg a .png, molto piu' comodo da usare).
            image = image[:-4]
            print('{img_name} crawled.'.format(img_name=image))

            # imread() legge l'immagine specificata dal path, imsave la salva. Per risolvere il viola/giallo
            # ho pensato di ricaricare l'immagine e salvarla con un altro formato tramite PIL (incompatibile
            # con plt). Infine, os si occupa di rimuovere l'immagine di troppo (quella gialla/viola).
            # So che e' un metodo molto macchinoso, ma va fatto una sola volta, quindi non ho badato molto
            # all'ottimizzazione. Se ti viene in mente qualcosa di meglio, ben venga!

            img = cv.imread('{read_path}/{img_name}.jpg'.format(read_path=self.read_path, img_name=image))

            # threshold() funziona cosi':
            # - img indica l'immagine di cui fare il threshold.
            # - 115 e' un numero che va da 0 a 255 (<- possibili livelli di colore) e indica la soglia oltre la
            #   quale il pixel deve essere reso grigio piuttosto che bianco. Abbassare questo parametro significa
            #   considerare solo pixel via via piu' scuri, viceversa alzandolo si considerano anche pixel sempre
            #   piu' chiari. Agisci su questo parametro.
            # - 255 e' il numero massimo di tonalita' di colore (insomma, 8 bit).
            # - cv.THRESH_BINARY_INV permette di binarizzare l'immagine e invertire il risultato. cv.THRESH_BINARY
            #   fa la stessa cosa, ma inverte la colorazione dei pixel. Ce ne sono altre, divertitici se vuoi.

            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            _, thresh1 = cv.threshold(gray, 120, 255, cv.THRESH_BINARY_INV)
            cv.imwrite('{save_path}/{img_name}.png'.format(save_path=self.save_path, img_name=image), thresh1)

            print('{img_name} binarized.'.format(img_name=image))

    def rotateOriginals(self, image_path, nPage, angles):

        img = cv.imread(image_path)

        # Converte l'immagine in scala di grigi
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Binarizzazione
        th, threshed = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)

        # Rotazione con minAreaRect on the nozeros
        pts = cv.findNonZero(threshed)
        ret = cv.minAreaRect(pts)

        (cx, cy), (w, h), ang = ret
        if w > h:
            w, h = h, w
            ang += 90

        ang = angles[str(nPage)]

        M = cv.getRotationMatrix2D((cx, cy), ang, 1.0)
        rotated = cv.warpAffine(img, M, (img.shape[1], img.shape[0]))

        cv.imwrite('GenesisPages/old/MuenchenRotated/Gut-{nPage}.png'.format(nPage=nPage), rotated)



    def linesCropping(self, image_path, nPage, firstColumn, secondColumn, dictionary, angles, wordPositions, frequentWord):

        #user = input('Inserire utente (scelte possibili: Federico, Francesco): ')
        user = ' '

        img = cv.imread(image_path)
        cropped = cv.imread('cropped.png')
        cropped2 = cv.imread('cropped2.png')
        cropped2 = cv.imread('cropped4.png')

        # Converte l'immagine in scala di grigi
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Binarizzazione
        th, threshed = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)

        #cv.imwrite('threshed.jpg', threshed)

        # Rotazione con minAreaRect on the nozeros
        pts = cv.findNonZero(threshed)
        ret = cv.minAreaRect(pts)

        (cx, cy), (w, h), ang = ret
        if w > h:
            w, h = h, w
            ang += 90

        # carica l'angolo giusto, trovato con findRotationAngle e salvato in precedenza in json
        ang = angles[str(nPage)]

        M = cv.getRotationMatrix2D((cx, cy), ang, 1.0)
        rotated = cv.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

        # Fa l'istogramma, conta i punti neri per ogni riga. Picchi di neri corrispondono alla stessa
        hist = cv.reduce(rotated, 1, cv.REDUCE_AVG).reshape(-1)
        histVert = self.histogramV(rotated)

        th, rotated = cv.threshold(rotated, 140, 255, cv.THRESH_BINARY)

        # Questa e' la soglia che decide fino a che punto tagliare

        th = 8
        if nPage is 15:
            th = 20
        if nPage is 16:
            th = 13
        if nPage is 18:
            th = 9
        if nPage is 20:
            th = 7
        if nPage is 21:
            th = 14
        if nPage is 23:
            th = 11
        if nPage is 25:
            th = 15
        if nPage is 26:
            th = 11
        if nPage is 27:
            th = 5
        if nPage is 30:
            th = 9
        if nPage is 31:
            th = 14
        if nPage is 33:
            th = 8

        # Coordinate dell'immagine, altezza larghezza
        H, W = img.shape[:2]
        # decido di tagliare se il valore dell'istogramma rientra nella soglia
        uppers = [y for y in range(H - 1) if hist[y] <= th and hist[y + 1] > th]
        lowers = [y for y in range(H - 1) if hist[y] > th and hist[y + 1] <= th]
        columns = [y for y in range(W - 1) if (histVert[y] == 1250 and
                                               histVert[y] > histVert[y + 1]) or
                   (histVert[y] == 1250 and
                    histVert[y] > histVert[y - 1])]

        self.lineRepairUnder(uppers, lowers, 45)

        # traccia semplicemente la linea, del colore desiderato
        rotated = cv.cvtColor(rotated, cv.COLOR_GRAY2BGR)
        for y in uppers:
            cv.line(rotated, (0, y), (W, y), (255, 0, 0), 1)

        for y in lowers:
            cv.line(rotated, (0, y), (W, y), (0, 255, 0), 1)

        # Pagine dispari con colonne non tagliate bene
        if (len(columns) is not 4 and (nPage % 2) is 1):
            columns = []
            columns.append(120)
            columns.append(500)
            columns.append(520)
            columns.append(880)

        # Pagine pari con colonne non tagliate bene
        if (len(columns) is not 4 and (nPage % 2) is 0):
            columns = []
            columns.append(50)
            columns.append(440)
            columns.append(450)
            columns.append(840)

        leftColumn = rotated[:, columns[0]:columns[1]]
        rightColumn = rotated[:, columns[2]:columns[3]]

        if user == 'Federico' and frequentWord is None:
            resizedLeft = cv.resize(leftColumn, (int(450*(13/25)), int(1250*(13/25))))
            resizedRight = cv.resize(rightColumn, (int(450*(13/25)), int(1250*(13/25))))

            cv.imshow(firstColumn, resizedLeft)
            cv.moveWindow(firstColumn, 100, 100)
            cv.imshow(secondColumn, resizedRight)
            cv.moveWindow(secondColumn, 900, 100)
            cv.waitKey(0)
        elif frequentWord is None:
            cv.imshow(firstColumn, leftColumn)
            cv.imshow(secondColumn, rightColumn)

        # Decommentare per salvare la pagina intera con line segmentation
        #cv.imwrite('GenesisPages/old/MuenchenLineSegmentation/Gut-{nPage}.png'.format(nPage=nPage), rotated)
        #return

        xBegin = []
        xEnd = []
        # Colonna di sinistra
        j = 0
        for i in range(len(uppers)):

            listBegin, listEnd, j = self.wordSegmentation(leftColumn[uppers[i]: lowers[i], :], cropped, cropped2, j, dictionary,
                                                       firstColumn, user, wordPositions, frequentWord)
            if listBegin is not None:
                xBegin.append(listBegin)
                xEnd.append(listEnd)

        #cv.imshow(secondColumn, rightColumn)
        #cv.waitKey(0)

        # Colonna di destra
        j = 0
        for i in range(len(uppers)):
            listBegin, listEnd, j = self.wordSegmentation(rightColumn[uppers[i]: lowers[i], :], cropped, cropped2, j, dictionary,
                                                       secondColumn, user, wordPositions, frequentWord)
            if listBegin is not None:
                xBegin.append(listBegin)
                xEnd.append(listEnd)


    def lineRepairUnder(self, uppers, lowers, th):

        # Ripara l'under
        for i in range(len(uppers) - 1):
            if (uppers[i + 1] - uppers[i] > th):
                uppers.insert(i + 1, uppers[i] + 25)
            if (lowers[i + 1] - lowers[i] > th):
                lowers.insert(i + 1, lowers[i] + 25)

    def lineRepairOver(self, uppers, lowers):

        # Ripara linee troppo vicine
        th = 6
        for i in range(len(uppers) - 1):
            try:
                if (uppers[i + 1] - uppers[i] < th):
                    uppers.remove(uppers[i + 1])
                if (lowers[i + 1] - lowers[i] < th):
                    lowers.remove(lowers[i + 1])
            except IndexError:
                break

    def wordSegmentation(self, line, cropped, cropped2, i, dictionary, nColumn, user, wordPositions, frequentWord):

        # A questo punto dobbiamo fare un'istogramma proiettando verticalmente. Pero' va fatto PER OGNI riga trovata
        # in precedenza... Si puo' utilizzare anche la funzione reduce come in precedenza, ma non mi tornava e quindi
        # mi sono scritto un istogramma a mano

        # Proiezione verticale
        H, W = line.shape[:2]

        # Per evitare problemi di oversegmentation, se trovo una linea troppo fine, la salto
        if (H < 5):
            return None, None, i

        if frequentWord is None:
            cv.imshow('Line', line)
            if user == 'Federico':
                cv.moveWindow('Line', 490, 300)

        lineHistRow = self.histogram(line)

        # Valore di soglia
        thW = 2
        listBegin = [x for x in range(W - 1) if lineHistRow[x] <= thW and lineHistRow[x + 1] > thW]
        listEnd = [x for x in range(W - 1) if lineHistRow[x] > thW and lineHistRow[x + 1] <= thW]

        # Per ora meglio calimero semplice

        caliList = self.calimero(line, cropped)
        #caliList = self.two_way_calimero(line, cropped, cropped2)

        for j in range(1, len(caliList)):
            try:
                if caliList[j - 1][0] - caliList[j][0] < 10:
                    caliList.pop(j)
            except IndexError:
                continue

        for j in range(len(caliList)):
            try:
                listBegin.append(caliList[j][0] + 6)
                listEnd.append(caliList[j][0])
            except IndexError:
                break

        listBegin.sort()
        listEnd.sort()

        # Stampa a schermo tagliando la riga con i valori ottenuti

        try:
            wordsInLine = dictionary[nColumn][i]
        except IndexError:
            wordsInLine = 6

        listBegin, listEnd = self.kBestCuts(line, listBegin, listEnd, wordsInLine)

        for j in range(len(listBegin)):
            try:
                word = line[:, listBegin[j]: listEnd[j]]
            except IndexError:
                break

            h, w = word.shape[:2]
            if (h > 0 and w > 0):
                if frequentWord is None:
                    cv.imshow('Word', word)
                    if user == 'Federico':
                        cv.moveWindow('Word', 500, 500)
                    cv.waitKey(0)

                elif str((nColumn, i, j)) in wordPositions.keys():
                    cv.imwrite('frequentWords/{frequentWord}/{nColumn}_{i}_{j}.png'.format(frequentWord=frequentWord,
                                                                                           nColumn=nColumn, i=i, j=j),
                               word)
        i += 1

        return listBegin, listEnd, i


    def histogram(self, image):

        H, W = image.shape[:2]

        histogram = []
        for i in range(W):
            histogram.append(0)
            for j in range(H):
                if image[j, i][0] == 0:
                    continue
                else:
                    histogram[i] += 1

        return histogram


    def histogramV(self, image):

        H, W = image.shape[:2]

        th, threshed = cv.threshold(image, 127, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

        histogram = []

        for i in range(W):
            histogram.append(0)
            for j in range(H):
                if threshed[j, i] <= 29:
                    continue
                else:
                    histogram[i] += 1

        return histogram


    # TODO: usa le componenti connesse
    def calimero(self, image, cropped):

        method = cv.TM_SQDIFF_NORMED

        result = cv.matchTemplate(cropped, image, method)

        threshold = 0.76    # best atm: 0.76
        loc = np.where(result < threshold)
        pts = []
        for pt in zip(*loc[::-1]):  # Switch columns and rows
            try:
                if np.all(image[(pt[1] + 8), (pt[0] + 3)]) == 0 and np.all(image[(pt[1] - 8), (pt[0] + 3)]) == 0:
                    # cv.rectangle(image, pt, (pt[0] + 6, pt[1] + 7), (0, 0, 255), 2)
                    pts.append(pt)
            except IndexError:
                break

        # Save the original image with the rectangle around the match.
        # cv.imwrite('calimered.png', image)

        return pts

    def true_calimero(self, img):

        blur_radius = 1.0
        threshold = 80  # 80 con gauss filtering

        print(img.shape)

        #imgf = ndimage.gaussian_filter(img, blur_radius)

        labeled, nr_objects = ndimage.label(img > threshold)
        print("Number of objects is %d " % nr_objects)

        coords = []
        for x in range(nr_objects):
            coords = np.where(np.any(labeled == x, -1))[0]
            cv.rectangle(labeled, (coords[x], coords[x]), (coords[x] + 3, coords[x] + 3),
                         (0, 255, 0), thickness=2)

        print(coords)

        plt.imsave('temp/out.png', labeled)

    # Funzione che decide quali tagli togliere seguendo un'euristica: ordina i tagli in base alla differenza tra il
    # precedente e il successivo. Quelli con distanza minore sono i canditati ad essere tolti; prende in ingresso il
    # numero di parole della riga, note attraverso il groundTruth. Andra' usato combinatamente con CALIMERO.

    def kBestCuts(self, line, listBegin, listEnd, nWords):

        # Caso in cui non posso tagliare con le parole

        if(len(listEnd) > len(listBegin)):
            listEnd.pop(0)

        if nWords is len(listBegin) or nWords > len(listBegin):
            return listBegin, listEnd

        listDiff = []

        for i in range(1, len(listBegin)):
            listDiff.append(listBegin[i] - listEnd[i - 1])

        orderedList = sorted(listDiff)

        nCuts = len(listBegin) - nWords
        for k in range(nCuts):
            i = listDiff.index(orderedList[0])
            try:
                listEnd[i] = listEnd[i + 1]
                listBegin[i + 1] = None
                listEnd[i + 1] = None
                listDiff[i] = None
            except IndexError:
                continue

            listBegin.remove(None)
            listEnd.remove(None)

            listDiff = []

            for i in range(1, len(listBegin)):
                listDiff.append(listBegin[i] - listEnd[i - 1])

            orderedList = sorted(listDiff)

        '''
        nCuts = len(listBegin) - nWords
        while nCuts > 0:
            for i in range(len(listDiff)):
                if listDiff[i] is 1:
                    try:
                        listEnd[i] = listEnd[i + 1]
                        listBegin[i + 1] = None
                        listEnd[i + 1] = None
                        listDiff[i] = None
                        break
                    except IndexError:
                        break
            try:
                listBegin.remove(None)
                listEnd.remove(None)
            except ValueError:
                nCuts -= 1
                break
            nCuts -= 1

        '''

        return listBegin, listEnd

    def getRotationMatrix(self, center, angle, scale):

        M = []
        M.append([])
        M.append([])

        alpha = -(scale * math.cos(angle))
        beta = scale * math.sin(angle)

        M[0].append(alpha)
        M[0].append(beta)
        M[0].append(((1 - alpha) * center[0] - beta * center[1]))
        M[1].append(-beta)
        M[1].append(alpha)
        M[1].append((beta * center[0] + (1 - alpha) * center[1]))

        M = np.asarray(M)

        return M


    def findRotationAngle(self, image_path):

        # Idea: trova il primo punto bianco della prima riga a sx e il primo punto bianco dell'ultima riga a sx,
        #       calcola le distanze, l'ipotenusa e determina sin, cos dell'angolo. Usa arcsin e arccos per
        #       trovare l'angolo e restituiscilo

        image = cv.imread(image_path, 0)

        img_path = image_path[image_path.find('Gut'):]

        _, thresh1 = cv.threshold(image, 70, 255, cv.THRESH_BINARY_INV)
        img_path = img_path[:img_path.find('.jpg')]
        plt.imsave('temp/{img_name}.jpg'.format(img_name=img_path), thresh1)

        imgx = Image.open('temp/{img_name}.jpg'.format(img_name=img_path)).convert('LA')

        imgx.save('temp/{img_name}.png'.format(img_name=img_path))
        os.remove('temp/{img_name}.jpg'.format(img_name=img_path))

        threshed = cv.imread('temp/{img_name}.png'.format(img_name=img_path))

        H, W = threshed.shape[:2]

        # Modo complesso: usando le distanze dai due angoli
        distances = []
        topLeftCornerX = 0
        topLeftCornerY = 0
        firstWhite = False
        for x in range(W):
            whitePixels = 0
            for y in range(H):
                if threshed[y][x][0] >= 200:
                    whitePixels += 1
            if whitePixels >= 10:
                for y in range(W):
                    if threshed[y][x][0] >= 200 and not firstWhite:
                        distances.append((math.sqrt(math.pow(x - topLeftCornerX, 2) + math.pow(y - topLeftCornerY, 2)), x, y))
                        firstWhite = True
            firstWhite = False

        dist = np.zeros(len(distances))
        for x in range(len(distances)):
            dist[x] = (distances[x][0])
        minDist = np.argmin(dist)

        topLeftX = distances[int(minDist)][1]
        topLeftY = distances[int(minDist)][2]

        distances = []
        bottomLeftCornerRow = 1250
        bottomLeftCornerCol = 0
        firstWhite = False
        for row in range(H - 1, 0, -1):
            whitePixels = 0
            for col in range(W):
                if threshed[row][col][0] >= 200:
                    whitePixels += 1
            if whitePixels >= 50:
                for col2 in range(W):
                    if threshed[row][col2][0] >= 200 and not firstWhite:
                        distances.append((math.sqrt(math.pow(bottomLeftCornerRow - row, 2) + math.pow(bottomLeftCornerCol - col2, 2)), row, col2))
                        firstWhite = True

            firstWhite = False

        dist = np.zeros(len(distances))
        for x in range(len(distances)):
            dist[x] = (distances[x][0])
        minDist = np.argmin(dist)

        bottomLeftX = distances[int(minDist)][2]
        bottomLeftY = distances[int(minDist)][1]

        cv.line(threshed, (topLeftCornerX, topLeftCornerY), (topLeftX, topLeftY) , color=(0, 255, 0), thickness=1)
        cv.line(threshed, (bottomLeftCornerCol, bottomLeftCornerRow), (bottomLeftX, bottomLeftY) , color=(0, 255, 0), thickness=1)
        cv.rectangle(threshed, (topLeftX, topLeftY), (topLeftX+2, topLeftY+2), color=(0, 0, 255), thickness=4)
        cv.rectangle(threshed, (bottomLeftX, bottomLeftY), (bottomLeftX+2, bottomLeftY+2), color=(0, 0, 255), thickness=4)
        pt1 = (topLeftX, topLeftY)
        pt2 = (bottomLeftX, bottomLeftY)
        pt3 = (bottomLeftX, topLeftY)
        cv.line(threshed, pt1, pt2, color=(0, 255, 0), thickness=2)
        cv.line(threshed, pt2, pt3, color=(0, 255, 0), thickness=2)
        cv.line(threshed, pt3, pt1, color=(0, 255, 0), thickness=2)

        # resized = cv.resize(threshed, (int(900*(13/25)), int(1250*(13/25))))
        # cv.imshow('page', resized)
        # cv.waitKey(0)

        # calcolo le lunghezze dei cateti
        d_pt2pt3 = math.fabs(topLeftY - bottomLeftY)
        d_pt1pt3 = math.fabs(topLeftX - bottomLeftX)
        # teorema di pitagora per trovare l'ipotenusa
        d_pt1pt2 = math.sqrt(math.pow(d_pt2pt3, 2) + math.pow(d_pt1pt3, 2))
        # definizione di coseno
        angleCos = d_pt2pt3 / d_pt1pt2
        # converto da radianti il risultato dell'arccos ottenuto prima
        rotationAngle = math.degrees(math.acos(angleCos))
        if bottomLeftX > topLeftX:
            rotationAngle = - rotationAngle

        os.remove('temp/{img_name}.png'.format(img_name=img_path))

        return rotationAngle

    def two_way_calimero(self, image, cropped1, cropped2):

        method = cv.TM_SQDIFF_NORMED

        result = cv.matchTemplate(cropped1, image, method)

        threshold = 0.76    # best atm: 0.76
        loc = np.where(result < threshold)
        pts = []
        for pt in zip(*loc[::-1]):  # Switch columns and rows
            try:
                if np.all(image[(pt[1] + 8), (pt[0] + 3)]) == 0 and np.all(image[(pt[1] - 8), (pt[0] + 3)]) == 0:
                    pts.append(pt)
            except IndexError:
                break

        result = cv.matchTemplate(cropped2, image, method)

        threshold2 = 0.3
        loc = np.where(result < threshold2)
        pts2 = []
        for pt in zip(*loc[::-1]):  # Switch columns and rows
            try:
                if np.all(image[(pt[1] + 8), (pt[0] + 3)]) == 0 and np.all(image[(pt[1] - 8), (pt[0] + 3)]) == 0:
                    pts2.append(pt)
            except IndexError:
                break

        finalPts = [pt for pt in pts2 if pt not in pts]

        for pt in pts:
            finalPts.append(pt)

        """for pt in finalPts:
            cv.rectangle(image, pt, (pt[0] + 6, pt[1] + 7), (0, 0, 255), 2)"""

        # Save the original image with the rectangle around the match.
        # cv.imwrite('two_way_calimered.png', image)

        return finalPts
