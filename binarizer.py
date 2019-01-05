import cv2 as cv
import os
import imutils
import numpy as np
import math

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

            img = cv.imread('{read_path}/{img_name}.jpg'.format(read_path=self.read_path, img_name=image), 0)

            # threshold() funziona cosi':
            # - img indica l'immagine di cui fare il threshold.
            # - 115 e' un numero che va da 0 a 255 (<- possibili livelli di colore) e indica la soglia oltre la
            #   quale il pixel deve essere reso grigio piuttosto che bianco. Abbassare questo parametro significa
            #   considerare solo pixel via via piu' scuri, viceversa alzandolo si considerano anche pixel sempre
            #   piu' chiari. Agisci su questo parametro.
            # - 255 e' il numero massimo di tonalita' di colore (insomma, 8 bit).
            # - cv.THRESH_BINARY_INV permette di binarizzare l'immagine e invertire il risultato. cv.THRESH_BINARY
            #   fa la stessa cosa, ma inverte la colorazione dei pixel. Ce ne sono altre, divertitici se vuoi.

            _, thresh1 = cv.threshold(img, 70, 255, cv.THRESH_BINARY_INV) # 55 per Goet, 115 per Muen (sperimentali).
            plt.imsave('{save_path}/{img_name}.jpg'.format(save_path=self.save_path, img_name=image), thresh1)

            # Qui viene ricaricata l'immagine con l'altra libreria.
            imgx = Image.open('{save_path}/{img_name}.jpg'.format(save_path=self.save_path, img_name=image)).convert('LA')

            imgx.save('{save_path}/{img_name}.png'.format(save_path=self.save_path, img_name=image))

            # A questo punto ci sono due copie di ciascuna immagine: una gialla e viola in .jpg e una grigia e
            # bianca in .png. Ci e' utile la seconda, quindi vengono eliminate le immagini inutili.

            os.remove('{save_path}/{img_name}.jpg'.format(save_path=self.save_path, img_name=image))

            print('{img_name} binarized.'.format(img_name=image))

    # TODO: automatizzare il modo per ottenere una rotazione corretta.
    # IDEA: se calcolo quanti sono i pixel antecedenti alla prima parola della prima riga e quanti quelli antecedenti
    #       alla prima parola dell'ultima riga, posso fare un rapporto tra le quantita' e capire di quanto ruotare
    #       l'immagine per farla venire dritta. E' molto rozzo come approccio, ma non credo che abbiamo bisogno di
    #       una precisione estrema, almeno per le colonne.

    def rotate(self, image_path):

        # Carico l'immagine e la ruoto alla "come viene viene"

        img = cv.imread(image_path)
        rotated = imutils.rotate(img, 1)
        cv.imwrite('rotated.png', rotated)

        # Riapro l'immagine con l'altra libreria (sempre per la storia dell'incompatibilita' tra le due), la converto
        # in array e separo i canali (R,G,B,alpha)

        img = Image.open('rotated.png')
        img = img.convert('RGBA')
        data = np.array(img)
        red, green, blue, alpha = data.T

        # Individuo le aree nere e le sostituisco col grigio di fondo (29, 29, 29) che ho trovato debuggando e
        # leggendo gli elementi dell'array

        black_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][black_areas.T] = (29, 29, 29)

        # Riconverto l'immagine e la sovrascrivo a quella sbagliata

        img = Image.fromarray(data)
        img.save('rotated.png')


    def linesCropping(self, image_path, nPage, firstColumn, secondColumn, dictionary):

        img = cv.imread(image_path)
        cropped = cv.imread('cropped.png')

        # Converte l'immagine in scala di grigi
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Binarizzazione
        th, threshed = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

        # Rotazione con minAreaRect on the nozeros
        pts = cv.findNonZero(threshed)
        ret = cv.minAreaRect(pts)

        (cx, cy), (w, h), ang = ret
        #ang = self.findRotationAngle(threshed)
        if w > h:
            w, h = h, w
            ang += 90

        # Per ora mettiamo un angolo a mano, poi si vedra'
        if nPage is 14:
            ang = -0.8
        if nPage is 18:
            ang = -0.5
        if nPage is 19:
            ang = 0.6
        if nPage is 21:
            ang = 1.5
        if nPage is 24:
            ang = -0.4
        if nPage is 26:
            ang = -0.55
        if nPage is 30:
            ang = 0.2
        if nPage is 31:
            ang = 0

        ## Find rotated matrix, do rotation
        M = cv.getRotationMatrix2D((cx, cy), ang, 1.0)
        rotated = cv.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

        # Fa l'istogramma, conta i punti neri per ogni riga. Picchi di neri corrispondono alla stessa
        hist = cv.reduce(rotated, 1, cv.REDUCE_AVG).reshape(-1)
        histVert = self.histogramV(rotated)

        # Questa e' la soglia che decide fino a che punto tagliare

        th = 8
        if nPage is 15:
            th = 20
        if nPage is 16:
            th = 9
        if nPage is 17:
            th = 9
        if nPage is 20:
            th = 11
        if nPage is 21:
            th = 14
        if nPage is 23:
            th = 14
        if nPage is 25:
            th = 17
        if nPage is 26:
            th = 11

        # Limito il numero di righe da poter fare in verticale
        numLines = 0
        maxNumLines = 4

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

        # "line" credo che tracci semplicemente la linea, del colore desiderato
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

        '''
                for x in columns:
            if numLines < maxNumLines:
                cv.line(rotated, (x, 0), (x, H), (0, 0, 255), 1)
                numLines += 1
        '''

        leftColumn = rotated[:, columns[0]:columns[1]]
        rightColumn = rotated[:, columns[2]:columns[3]]

        cv.imshow(firstColumn, leftColumn)
        cv.imshow(secondColumn, rightColumn)
        cv.waitKey(0)

        xBegin = []
        xEnd = []
        # Colonna di sinistra
        j = 0
        for i in range(len(uppers)):
            listBegin, listEnd, j = self.wordSegmentation(leftColumn[uppers[i]: lowers[i], :], cropped, j, dictionary,
                                                       firstColumn)
            if listBegin is not None:
                xBegin.append(listBegin)
                xEnd.append(listEnd)

        cv.imshow(secondColumn, rightColumn)
        cv.waitKey(0)

        # Colonna di destra
        j = 0
        for i in range(len(uppers)):
            listBegin, listEnd, j = self.wordSegmentation(rightColumn[uppers[i]: lowers[i], :], cropped, j, dictionary,
                                                       secondColumn)
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

    def wordSegmentation(self, line, cropped, i, dictionary, nColumn):

        # A questo punto dobbiamo fare un'istogramma proiettando verticalmente. Pero' va fatto PER OGNI riga trovata
        # in precedenza... Si puo' utilizzare anche la funzione reduce come in precedenza, ma non mi tornava e quindi
        # mi sono scritto un istogramma a mano

        # Proiezione verticale
        H, W = line.shape[:2]

        # Per evitare problemi di oversegmentation, se trovo una linea troppo fine, la salto
        if (H < 5):
            return None, None, i

        cv.imshow('Line', line)
        cv.waitKey(0)

        lineHistRow = self.histogram(line)

        # Valore di soglia
        thW = 2
        listBegin = [x for x in range(W - 1) if lineHistRow[x] <= thW and lineHistRow[x + 1] > thW]
        listEnd = [x for x in range(W - 1) if lineHistRow[x] > thW and lineHistRow[x + 1] <= thW]

        caliList = self.calimero(line, cropped)

        for j in range(1, len(caliList)):
            try:
                if caliList[j - 1][0] - caliList[j][0] < 10:
                    caliList.pop(j)
            except IndexError:
                break

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
                cv.imshow('Word', word)
                cv.waitKey(0)
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


    def calimero(self, image, cropped):

        method = cv.TM_SQDIFF_NORMED

        w, h = cropped.shape[:-1]
        wImage, hImage = image.shape[:-1]

        if (w <= wImage or h <= hImage):
            return []

        result = cv.matchTemplate(cropped, image, method)

        threshold = 0.22    # best atm: 0.21
        loc = np.where(result < threshold)
        pts = []
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            try:
                if np.all(image[(pt[1] + 8), (pt[0] + 3)]) == 0 and np.all(image[(pt[1] - 8), (pt[0] + 3)]) == 0:
                    #cv.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                    pts.append(pt)
            except IndexError:
                break

        # Save the original image with the rectangle around the match.
        #cv.imwrite('calimered.png', image)
        return pts


    # Funzione che decide quali tagli togliere seguendo un'euristica: ordina i tagli in base alla differenza tra il
    # precedente e il successivo. Quelli con distanza minore sono i canditati ad essere tolti; prende in ingresso il
    # numero di parole della riga, note attraverso il groundTruth. Andra' usato combinatamente con CALIMERO.

    def kBestCuts(self, line, listBegin, listEnd, nWords):

        # nWords = 14

        # Caso in cui non posso tagliare con le parole, ma posso fare calimero

        if nWords is len(listBegin) or nWords > len(listBegin):
            return listBegin, listEnd

        listDiff = []
        for i in range(1, len(listBegin)):
            listDiff.append(listBegin[i] - listEnd[i - 1])

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

    #TODO: la funzione e' corretta, ma bisogna trovare il modo di identificare i due punti per bene
    def findRotationAngle(self, threshed):

        # Idea: trova il primo punto bianco della prima riga a sx e il primo punto bianco dell'ultima riga a sx,
        #       calcola le distanze, l'ipotenusa e determina sin, cos dell'angolo. Usa arcsin e arccos per
        #       trovare l'angolo e restituiscilo
        H, W = threshed.shape[:2]

        firstWhite = False
        firstWhite2 = False
        topLeftX = 0
        topLeftY = 0
        bottomLeftX = 0
        bottomLeftY = 0
        maxNumWhite = 0

        # Modo complesso: usando le distanze dai due angoli
        """distances = []
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

        cv.line(threshed, (topLeftCornerX, topLeftCornerY), (topLeftX, topLeftY) , color=(0, 255, 0), thickness=1)

        distances = []
        bottomLeftCornerX = 0
        bottomLeftCornerY = 1249
        firstWhite = False
        for x in range(W):
            whitePixels = 0
            for y in range(H - 1, 0, -1):
                if threshed[y][x][0] >= 200:
                    whitePixels += 1
            if whitePixels >= 10:
                for z in range(W):
                    if threshed[z][x][0] >= 200 and not firstWhite:
                        distances.append((math.sqrt(math.pow(x - bottomLeftCornerX, 2) + math.pow(bottomLeftCornerY - z, 2)), x, z))
                        firstWhite = True
            firstWhite = False

        dist = np.zeros(len(distances))
        for x in range(len(distances)):
            dist[x] = (distances[x][0])
        minDist = np.argmin(dist)

        bottomLeftX = distances[int(minDist)][1]
        bottomLeftY = distances[int(minDist)][2]

        cv.line(threshed, (bottomLeftCornerX, bottomLeftCornerY), (bottomLeftX, bottomLeftY) , color=(0, 255, 0), thickness=1)
        
        # evidenzio i due punti e il triangolo di rotazione (da togliere quando tutto funzionerà)
        cv.rectangle(threshed, (topLeftX, topLeftY), (topLeftX+2, topLeftY+2), color=(0, 0, 255), thickness=4)
        cv.rectangle(threshed, (bottomLeftX, bottomLeftY), (bottomLeftX+2, bottomLeftY+2), color=(0, 0, 255), thickness=4)
        cv.rectangle(threshed, (topLeftCornerX, topLeftCornerY), (topLeftCornerX+2, topLeftCornerY+2), color=(255, 0, 0), thickness=4)
        cv.rectangle(threshed, (bottomLeftCornerX, bottomLeftCornerY), (bottomLeftCornerX+2, bottomLeftCornerY+2), color=(255, 0, 0), thickness=4)"""
        """cv.line(threshed, pt1, pt2, color=(0, 255, 0), thickness=1)
        cv.line(threshed, pt2, pt3, color=(0, 255, 0), thickness=1)
        cv.line(threshed, pt3, pt1, color=(0, 255, 0), thickness=1)"""

        # Modo semplice: con due righe fissate
        for x in range(W):
            if threshed[145][x][0] >= 200 and not firstWhite:
                firstWhite = True
                topLeftX = x
                break
        topLeftY = 145

        # E' uno schifo, ma funziona in teoria
        firstWhite = False
        if topLeftX >= 150:
            for x in range(W):
                if threshed[155][x][0] >= 200 and not firstWhite:
                    firstWhite = True
                    topLeftX = x
                    break
            topLeftY = 155

        firstWhite = False
        if topLeftX >= 150:
            for x in range(W):
                if threshed[165][x][0] >= 200 and not firstWhite:
                    firstWhite = True
                    topLeftX = x
                    break
            topLeftY = 165

        firstWhite = False
        if topLeftX >= 150:
            for x in range(W):
                if threshed[200][x][0] >= 200 and not firstWhite:
                    firstWhite = True
                    topLeftX = x
                    break
            topLeftY = 200

        firstWhite = False
        for x in range(W):
            if threshed[540][x][0] >= 200 and not firstWhite:
                firstWhite = True
                bottomLeftX = x
                break
        bottomLeftY = 540

        if bottomLeftX >= 150:
            firstWhite = False
        for x in range(W):
            if threshed[550][x][0] >= 200 and not firstWhite:
                firstWhite = True
                bottomLeftX = x
                break
            bottomLeftY = 550

        if bottomLeftX >= 150:
            firstWhite = False
        for x in range(W):
            if threshed[560][x][0] >= 200 and not firstWhite:
                firstWhite = True
                bottomLeftX = x
                break
            bottomLeftY = 560

        if bottomLeftX >= 150:
            firstWhite = False
        for x in range(W):
            if threshed[610][x][0] >= 200 and not firstWhite:
                firstWhite = True
                bottomLeftX = x
                break
            bottomLeftY = 610


        cv.rectangle(threshed, (topLeftX, topLeftY), (topLeftX+2, topLeftY+2), color=(0, 0, 255), thickness=4)
        cv.rectangle(threshed, (bottomLeftX, bottomLeftY), (bottomLeftX+2, bottomLeftY+2), color=(0, 0, 255), thickness=4)
        pt1 = (topLeftX, topLeftY)
        pt2 = (bottomLeftX, bottomLeftY)
        pt3 = (bottomLeftX, topLeftY)
        cv.line(threshed, pt1, pt2, color=(0, 255, 0), thickness=1)
        cv.line(threshed, pt2, pt3, color=(0, 255, 0), thickness=1)
        cv.line(threshed, pt3, pt1, color=(0, 255, 0), thickness=1)

        resized = cv.resize(threshed, (int(900*(13/25)), int(1250*(13/25))))
        cv.imshow('pt', resized)
        cv.waitKey(0)

        # calcolo le lunghezze dei cateti
        d_pt2pt3 = math.fabs(topLeftY - bottomLeftY)
        d_pt1pt3 = math.fabs(topLeftX - bottomLeftX)
        # teorema di pitagora per trovare l'ipotenusa
        d_pt1pt2 = math.sqrt(math.pow(d_pt2pt3, 2) + math.pow(d_pt1pt3, 2))
        # definizione di coseno
        angleCos = d_pt2pt3 / d_pt1pt2
        # converto da radianti il risultato dell'arccos ottenuto prima
        rotationAngle = math.degrees(math.acos(angleCos))

        print(topLeftX, topLeftY)
        print(bottomLeftX, bottomLeftY)
        print(d_pt1pt2)
        print(d_pt1pt3)
        print(d_pt2pt3)
        print(rotationAngle)

        return rotationAngle