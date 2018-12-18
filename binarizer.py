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
        # quella già presente.

        if not os.path.exists(self.save_path):
            os.mkdir('{save_path}/'.format(save_path=self.save_path))
            print('Directory created.')
        else:
            print('Directory found.')

        for image in os.listdir('GenesisPages/old/{doc}/'.format(doc=self.bible)):

            # Rimuove il formato dalla stringa che identifica il nome dell'immagine (almeno dopo posso cambiare
            # da .jpg a .png, molto più comodo da usare).
            image = image[:-4]
            print('{img_name} crawled.'.format(img_name=image))

            # imread() legge l'immagine specificata dal path, imsave la salva. Per risolvere il viola/giallo
            # ho pensato di ricaricare l'immagine e salvarla con un altro formato tramite PIL (incompatibile
            # con plt). Infine, os si occupa di rimuovere l'immagine di troppo (quella gialla/viola).
            # So che è un metodo molto macchinoso, ma va fatto una sola volta, quindi non ho badato molto
            # all'ottimizzazione. Se ti viene in mente qualcosa di meglio, ben venga!

            img = cv.imread('{read_path}/{img_name}.jpg'.format(read_path=self.read_path, img_name=image), 0)

            # threshold() funziona così:
            # - img indica l'immagine di cui fare il threshold.
            # - 115 è un numero che va da 0 a 255 (<- possibili livelli di colore) e indica la soglia oltre la
            #   quale il pixel deve essere reso grigio piuttosto che bianco. Abbassare questo parametro significa
            #   considerare solo pixel via via più scuri, viceversa alzandolo si considerano anche pixel sempre
            #   più chiari. Agisci su questo parametro.
            # - 255 è il numero massimo di tonalità di colore (insomma, 8 bit).
            # - cv.THRESH_BINARY_INV permette di binarizzare l'immagine e invertire il risultato. cv.THRESH_BINARY
            #   fa la stessa cosa, ma inverte la colorazione dei pixel. Ce ne sono altre, divertitici se vuoi.

            _, thresh1 = cv.threshold(img, 115, 255, cv.THRESH_BINARY_INV) # 55 per Goet, 115 per Muen (sperimentali).
            plt.imsave('{save_path}/{img_name}.jpg'.format(save_path=self.save_path, img_name=image), thresh1)

            # Qui viene ricaricata l'immagine con l'altra libreria.
            imgx = Image.open('{save_path}/{img_name}.jpg'.format(save_path=self.save_path, img_name=image)).convert('LA')

            imgx.save('{save_path}/{img_name}.png'.format(save_path=self.save_path, img_name=image))

            # A questo punto ci sono due copie di ciascuna immagine: una gialla e viola in .jpg e una grigia e
            # bianca in .png. Ci è utile la seconda, quindi vengono eliminate le immagini inutili.

            os.remove('{save_path}/{img_name}.jpg'.format(save_path=self.save_path, img_name=image))

            print('{img_name} binarized.'.format(img_name=image))

    # TODO: automatizzare il modo per ottenere una rotazione corretta.
    # IDEA: se calcolo quanti sono i pixel antecedenti alla prima parola della prima riga e quanti quelli antecedenti
    #       alla prima parola dell'ultima riga, posso fare un rapporto tra le quantità e capire di quanto ruotare
    #       l'immagine per farla venire dritta. È molto rozzo come approccio, ma non credo che abbiamo bisogno di
    #       una precisione estrema, almeno per le colonne.

    def rotate(self, image_path):

        # Carico l'immagine e la ruoto alla "come viene viene"

        img = cv.imread(image_path)
        rotated = imutils.rotate(img, 1)
        cv.imwrite('rotated.png', rotated)

        # Riapro l'immagine con l'altra libreria (sempre per la storia dell'incompatibilità tra le due), la converto
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
