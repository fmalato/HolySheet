import cv2 as cv
import json
import pytesseract

def findCentroids(img):

    # convert image to grayscale image
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # convert the grayscale image to binary image
    ret, thresh = cv.threshold(gray_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)

    cv.imwrite('thresh.png', thresh)

    # calculate moments of binary image
    M = cv.moments(thresh)

    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # put text and highlight the center
    cv.circle(img, (cX, cY), 5, (255, 0, 0), -1)
    cv.putText(img, "centroid", (cX - 25, cY - 25), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv.imshow('centroids', img)
    cv.waitKey(0)

def imageGraph(image):

    height, width = image.shape[0], image.shape[1]

    graph = {}
    for row in range(height):
        line = []
        for col in range(width):
            if image[row][col][0] == 255:
                line.append(1)
            else:
                line.append(0)
        graph[row] = line

    visited = dfs(graph, 0, [])

    return visited


def dfs(graph, node, visited):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph, n, visited)
    return visited


def ccomps(img):

    # read the image and get the dimensions
    h, w, _ = img.shape # assumes color image

    # run tesseract, returning the bounding boxes
    boxes = pytesseract.image_to_boxes(img) # also include any config options you use

    # draw the bounding boxes on the image
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 1)

    # show annotated image and wait for keypress
    cv.imshow('image', img)
    cv.waitKey(0)

def hola(img):

    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

    cv.imshow('img', img)
    cv.waitKey(0)

from skimage import measure
from skimage import filters
import matplotlib.pyplot as plt
import numpy as np

def nTry():

    n = 12
    l = 256
    np.random.seed(1)
    im = np.zeros((l, l))
    points = l * np.random.random((2, n ** 2))
    im[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
    im = filters.gaussian_filter(im, sigma= l / (4. * n))
    blobs = im > 0.7 * im.mean()

    all_labels = measure.label(blobs)
    blobs_labels = measure.label(blobs, background=0)

    plt.figure(figsize=(9, 3.5))
    plt.subplot(131)
    plt.imshow(blobs, cmap='gray')
    plt.axis('off')
    plt.subplot(132)
    plt.imshow(all_labels, cmap='spectral')
    plt.axis('off')
    plt.subplot(133)
    plt.imshow(blobs_labels, cmap='spectral')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

