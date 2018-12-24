import binarizer as bin
import cv2 as cv


bible = 'Muenchen'
binar = bin.Binarizer(bible)

#binar.binarize()
#binar.rotate('image.png')
#binar.linesCropping('Gut-027.jpg')
img = cv.imread('threshed.png')
cropped = cv.imread('cropped.png')
binar.calimero(img, cropped)