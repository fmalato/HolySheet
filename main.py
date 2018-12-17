import cv2 as cv
import numpy as np

from matplotlib import pyplot as plt
from PIL import Image

img = cv.imread('bible.jpg', 0)

_, thresh1 = cv.threshold(img, 55, 255, cv.THRESH_BINARY_INV)
plt.imsave('ciao.jpg', thresh1)

imgx = Image.open('bible_binar.jpg').convert('LA')
imgx.save('ciao.png')
