import binarizer as bin
import cv2 as cv
import stringUtils


bible = 'Muenchen'
binar = bin.Binarizer(bible)

#binar.binarize()
#binar.rotate('image.png')
#binar.linesCropping('Gut-027.jpg')
#img = cv.imread('result.png')
#cropped = cv.imread('cropped.png')
#binar.calimero(img, cropped)

groundTruth = open("genesis1-20.txt", "r")
lines = groundTruth.readlines()

dictionary = stringUtils.getWordsCounterDict(lines)

print(dictionary)