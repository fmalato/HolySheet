import cv2 as cv
import os
import imutils
import numpy as np

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

            _, thresh1 = cv.threshold(img, 115, 255, cv.THRESH_BINARY_INV) # 55 per Goet, 115 per Muen (sperimentali).
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


    def linesCropping(self, image_path, firstColumn, secondColumn, dictionary):

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
        if w > h:
            w, h = h, w
            ang += 90

        ## Find rotated matrix, do rotation
        M = cv.getRotationMatrix2D((cx, cy), ang, 1.0)
        rotated = cv.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

        # Fa l'istogramma, conta i punti neri per ogni riga. Picchi di neri corrispondono alla stessa
        hist = cv.reduce(rotated, 1, cv.REDUCE_AVG).reshape(-1)
        histVert = self.histogramV(rotated)

        # Questa e' la soglia che decide fino a che punto tagliare
        th = 8

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

        # "line" credo che tracci semplicemente la linea, del colore desiderato
        rotated = cv.cvtColor(rotated, cv.COLOR_GRAY2BGR)
        for y in uppers:
            cv.line(rotated, (0, y), (W, y), (255, 0, 0), 1)

        for y in lowers:
            cv.line(rotated, (0, y), (W, y), (0, 255, 0), 1)

        for x in columns:
            if numLines < maxNumLines:
                cv.line(rotated, (x, 0), (x, H), (0, 0, 255), 1)
                numLines += 1

        xBegin = []
        xEnd = []

        leftColumn = rotated[:, columns[0]:columns[1]]
        rightColumn = rotated[:, columns[2]:columns[3]]

        # A questo punto dobbiamo fare un'istogramma proiettando verticalmente. Pero' va fatto PER OGNI riga trovata
        # in precedenza... Si puo' utilizzare anche la funzione reduce come in precedenza, ma non mi tornava e quindi
        # mi sono scritto un istogramma a mano

        for i in range(len(uppers)):
            line = leftColumn[uppers[i] : lowers[i], :]
            cv.imshow('second', line)
            # Proiezione verticale
            H, W = line.shape[:2]

            lineHistRow = self.histogram(line)

            # Valore di soglia
            thW = 2
            listBegin = [x for x in range(W - 1) if lineHistRow[x] <= thW and lineHistRow[x + 1] > thW]
            listEnd = [x for x in range(W - 1) if lineHistRow[x] > thW and lineHistRow[x + 1] <= thW]

            # Stampa a schermo tagliando la riga con i valori ottenuti

            listBegin, listEnd = self.kBestCuts(line, listBegin, listEnd, dictionary[firstColumn][i])

            caliList = self.calimero(line, cropped)

            print(caliList)

            for i in range(len(caliList)):
                try:
                    listBegin.append(caliList[i][0])
                    listEnd.append(caliList[i][0] + 6)
                except IndexError:
                    break

            listBegin.sort()
            listEnd.sort()

            print(listBegin)
            print(listEnd)

            for i in range(len(caliList)):
                try:
                    listEnd[listBegin.index(caliList[i][0]) - 1] -= 6
                    listBegin[listEnd.index(caliList[i][0] + 6) + 1] += 6
                except IndexError:
                    break

            print(listBegin)
            print(listEnd)

            for j in range(len(listBegin)):
                try:
                    word = line[:, listBegin[j] : listEnd[j]]
                except IndexError:
                    break
                h, w = word.shape[:2]
                if (h > 0 and w > 0):
                    cv.imshow('lol', word)
                    cv.waitKey(0)

            xBegin.append(listBegin)
            xEnd.append(listEnd)

        cv.imwrite("result.png", rotated)


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

        result = cv.matchTemplate(cropped, image, method)

        threshold = 0.21    # best atm: 0.21
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

