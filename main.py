import cv2 as cv
import numpy as np

from matplotlib import pyplot as plt

img = cv.imread('bible.jpg', 0)

ret, thresh1 = cv.threshold(img, 55, 255, cv.THRESH_BINARY_INV)

plt.imsave('bible_binar.jpg', thresh1)
