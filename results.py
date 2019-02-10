import json
import os
import cv2
import numpy as np

import utils

with open('results/bbox_genesis_2019_valid_results.json', 'r') as box:
    bboxes = json.load(box)

with open('results/genesis_valid_2019.json', 'r') as ann:
    annotations = json.load(ann)

with open('JsonUtils/10mostFrequentWords.json', 'r') as fw:
    frequentWordsDict = json.load(fw)

boundingBoxes = {}
for img in annotations['images']:
    image = cv2.imread('valid2019/{image_name}'.format(image_name=img['file_name']))
    image_id = int(img['file_name'].strip('.png')) + 188000
    boundingBoxes[image_id] = {}
    boundingBoxes[image_id]['bboxes'] = []
    boundingBoxes[image_id]['annotations'] = []
    #detections = []
    #groundTruth = []
    for el in bboxes:
        if el['image_id'] == image_id:
            cv2.rectangle(image, (int(el['bbox'][0]), int(el['bbox'][1])),
                      (int(el['bbox'][0] + el['bbox'][2]), int(el['bbox'][1] + el['bbox'][3])), (0, 255, 0), thickness=1)
            """cv2.putText(img=image, text=str(frequentWordsDict[el['category_id']]),
                        org=(int(el['bbox'][0]), int(el['bbox'][1]) - 5), fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=0.4, color=(0, 255, 0))"""
            #detections.append(el['bbox'])
            boundingBoxes[image_id]['bboxes'].append(el['bbox'])

    for x in annotations['annotations']:
        if x['image_id'] == image_id + 150:
            cv2.rectangle(image, (int(x['bbox'][0]), int(x['bbox'][1])),
                      (int(x['bbox'][0] + x['bbox'][2]), int(x['bbox'][1] + x['bbox'][3])), (0, 0, 255), thickness=1)
            """cv2.putText(img=image, text=str(frequentWordsDict[x['category_id']]),
                        org=(int(x['bbox'][0]), int(x['bbox'][1]) + int(x['bbox'][3] + 5)),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(0, 0, 255))"""
            #groundTruth.append(x['bbox'])
            boundingBoxes[image_id]['annotations'].append(x['bbox'])

    with open('bboxes.json', 'w+') as f:
        json.dump(boundingBoxes, f, indent=4)

    # TODO: funziona, ma potrebbe funzionare molto meglio con un sistema per trovare
    for box in boundingBoxes[image_id]['bboxes']:
        notes = []
        for ann in boundingBoxes[image_id]['annotations']:
            if (box[1] >= ann[1] - 20) and (box[1] <= ann[1] + 20):
                iou = utils.intersectionOverUnion(box, ann)
                if iou != 0.0 and ann not in notes:
                    print(ann, image_id)
                    if iou >= 0.5:
                        cv2.putText(img=image, text='Y',
                                    org=(int(box[0]), int(box[1]) + int(box[3] + 5)),
                                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255, 0, 0))
                        notes.append(ann)
                        break
                    else:
                        cv2.putText(img=image, text='N',
                                    org=(int(box[0]), int(box[1]) + int(box[3] + 5)),
                                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255, 0, 0))
                        notes.append(ann)
                        break


    """cv2.imshow('{image}'.format(image=img['file_name']), image)
    cv2.waitKey(100000)
    cv2.destroyAllWindows()"""

    cv2.imwrite('results/comparisons/comp_{n}'.format(n=img['file_name']), image)

