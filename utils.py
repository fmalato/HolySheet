import cv2 as cv
import json
import pytesseract
import numpy as np

from PIL import Image

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

# TODO: Find a solution to the conflict map problem.
# There should be 20 components, not 127

def connectedComponents(image_path):

    image = cv.imread(image_path)

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, threshed = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)    # BINARY non INV se gli si passa black n white

    height, width = image.shape[0], image.shape[1]
    numComponent = 0

    components = []
    conflicts = {}
    for row in range(height):
        line = []
        for col in range(width):
            if threshed[row][col] == 255 and (threshed[row][col - 1] == 255 or threshed[row - 1][col] == 255):
                line.append(numComponent)
            elif threshed[row][col] == 255 and (threshed[row][col - 1] == 0 and threshed[row - 1][col] == 0):
                numComponent += 1
                line.append(numComponent)
            elif threshed[row][col] == 0:
                line.append(0)
            if threshed[row][col] == 255 and (components[row - 1][col] != line[col - 1]) and \
                                            components[row - 1][col] != 0 and line[col - 1] != 0:
                rightOne = line[len(line) - 1]
                if rightOne not in conflicts.keys():
                    conflicts[rightOne] = []
                conflicts[rightOne].append(components[row - 1][col])
                line.pop(len(line) - 1)
                line.append(rightOne)
        components.append(line)

    for key in conflicts.keys():
        conflicts[key] = list(set(conflicts[key]))

    """for comp in components:
        for el in comp:
            if """

    image = []
    for comp in components:
        imgLine = []
        for el in comp:
            if el > 0 and el <= 10:
                imgLine.append((255, 0, 0))
            elif el > 10 and el <= 20:
                imgLine.append((0, 255, 0))
            elif el > 20:
                imgLine.append((0, 0, 255))
            else:
                imgLine.append((0, 0, 0))
        image.append(imgLine)

    imgArray = np.array(image, dtype=np.uint8)
    img = Image.fromarray(imgArray)

    img.save('generated.png')



