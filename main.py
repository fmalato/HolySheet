import binarizer as bin
import cv2 as cv
import stringUtils


bible = 'Muenchen'
binar = bin.Binarizer(bible)

#binar.binarize()
#binar.rotate('image.png')
#img = cv.imread('result.png')
#cropped = cv.imread('cropped.png')
#binar.calimero(img, cropped)

groundTruth = open("genesis1-20.txt", "r")
lines = groundTruth.readlines()

dictionary = stringUtils.getWordsCounterDict(lines)

binar.linesCropping('GenesisPages/old/Muenchen/Gut-027.jpg', "_P13_C0", "_P13_C1", dictionary)
