import cv2 as cv
import json
import collections
import os


def splitColumns(image_path, nPage, numImage):

    img = cv.imread(image_path)

    numCuts = 5
    imageHeight = 1250
    imageWidth = 900
    cutHeight = int(imageHeight/numCuts)
    cutWidth = int(imageWidth/2)

    # Odd pages are slightly off-centered
    if nPage % 2 is not 0:
        cutWidth = int(imageWidth/2 + 20)

    if not os.path.exists('testImages/'.format(nPage=nPage)):
        os.mkdir('testImages')
    if not os.path.exists('testImages/images_{nPage}'.format(nPage=nPage)):
        os.mkdir('testImages/images_{nPage}'.format(nPage=nPage))
    if not os.path.exists('test2019'):
        os.mkdir('test2019')

    # Divide the full image in 10 sub-images and saves them in train2019/ and in trainImages/
    with open('testImages/images_{nPage}/imgCoords.json'.format(nPage=nPage), 'w+') as f:
        for i in range(numCuts):
            cropped = img[i*cutHeight:(i+1)*cutHeight, 0:cutWidth]
            cv.imwrite('testImages/images_{nPage}/0000{x}.png'.format(nPage=nPage, x=i), cropped)
            json.dump((i*cutHeight, 0, cutWidth, cutHeight), f)
            f.write(', \n')
        for i in range(numCuts):
            cropped = img[i*cutHeight:(i+1)*cutHeight, cutWidth:imageWidth]
            cv.imwrite('testImages/images_{nPage}/0000{x}.png'.format(nPage=nPage, x=i+numCuts), cropped)
            json.dump((i * cutHeight, cutWidth, imageWidth - cutWidth, cutHeight), f)
            f.write(', \n')

    for i in range(numCuts):
        cropped = img[i*cutHeight:(i+1)*cutHeight, 0:cutWidth]
        cv.imwrite('test2019/{x}.png'.format(x=i+numImage-1), cropped)

    for i in range(numCuts):
        cropped = img[i*cutHeight:(i+1)*cutHeight, cutWidth:imageWidth]
        cv.imwrite('test2019/{x}.png'.format(x=i+numCuts+numImage-1), cropped)

    numImage += 2*numCuts

    return numImage


def COCOdataset():

    with open('annotationsTry.json') as instances:
        COCOGenesis = json.load(instances)

    id = 0
    for file in sorted(os.listdir('valid2019/')):
        img = cv.imread('valid2019/{file}'.format(file=file))
        height, width = img.shape[:2]
        COCOGenesis["images"].append({"license": 1,
                                      "file_name": file,
                                      "coco_url": "",
                                      "height": height,
                                      "width": width,
                                      "date_captured": "Today",
                                      "flickr_url": "",
                                      "id": 188000+id})
        id += 1

    with open('annotationsTry.json', 'w') as instances:
        json.dump(COCOGenesis, instances, indent=4)


def setAnnotations(nPage, cutWidthLeft, cutWidthRight, cutHeight, annotationId):

    numCuts = 5

    with open('inPagePositions.json') as pp:
        pagePositions = json.load(pp)
        pagePositions = collections.OrderedDict(pagePositions)

    with open('annotationsTry.json') as instances:
        COCOGenesis = json.load(instances)

    #for x in range(30, 34, 1):
    #    del pagePositions[str(x)]

    keys = [key for key in pagePositions[str(nPage)].keys()]
    for key in pagePositions[str(nPage)].keys():
        for coord in pagePositions[str(nPage)][key]:
            if coord[0] < cutWidthLeft:
                for x in range(numCuts):
                    if coord[1] <= (x + 1)*cutHeight and coord[1] >= x*cutHeight:
                        pagePos = x
                        posX = coord[0]
                        posY = coord[1] - (x)*cutHeight

                        COCOGenesis["annotations"].append({"id": annotationId,
                                                          "category_id": key,
                                                          "iscrowd": 0,
                                                          "segmentation": [[posX, posY, posX + coord[2], posY,
                                                                            posX + coord[2], posY +coord[3],
                                                                            posX, posY + coord[3]]],
                                                          "image_id": (nPage - 14)*10 + pagePos + 192000,
                                                          "area": coord[2]*coord[3],
                                                          "bbox": [posX, posY, coord[2], coord[3]]})
                        annotationId += 1
                        break
            if coord[0] >= cutWidthLeft:
                for x in range(numCuts):
                    if coord[1] <= (x + 1)*cutHeight and coord[1] >= x*cutHeight:
                        pagePos = x + numCuts
                        posX = coord[0] - cutWidthLeft
                        posY = coord[1] - (x) * cutHeight

                        COCOGenesis["annotations"].append({"id": annotationId,
                                                          "category_id": key,
                                                          "iscrowd": 0,
                                                          "segmentation": [[posX, posY, posX + coord[2], posY,
                                                                            posX + coord[2], posY +coord[3],
                                                                            posX, posY + coord[3]]],
                                                          "image_id": (nPage - 14)*10 + pagePos + 192000,
                                                          "area": coord[2]*coord[3],
                                                          "bbox": [posX, posY, coord[2], coord[3]]})
                        annotationId += 1
                        break

    for el in COCOGenesis["annotations"]:
        for key in keys:
            if el["category_id"] == key:
                el["category_id"] = keys.index(key)

    with open('annotationsTry.json', 'w+') as f:
        json.dump(COCOGenesis, f, indent=4)

    return annotationId






