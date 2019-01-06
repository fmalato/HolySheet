import binarizer as bin
import cv2 as cv
import stringUtils


bible = 'Muenchen'
binar = bin.Binarizer(bible)

#binar.binarize()

"""img = cv.imread('threshed.png')
cropped = cv.imread('cropped.png')
binar.calimero(img, cropped)"""

groundTruth = open("genesis1-20.txt", "r")
lines = groundTruth.readlines()

dictionary = stringUtils.getWordsCounterDict(lines)

# Problemi patologici su pag14, cattiva segmentazione su pag31

numPage = 15

binar.linesCropping('GenesisPages/old/Muenchen/Gut-0{x}.jpg'.format(x=numPage),
                    numPage,
                    '_P{x}_C0'.format(x=(numPage - 14)),
                    '_P{x}_C1'.format(x=(numPage - 14)),
                    dictionary)


