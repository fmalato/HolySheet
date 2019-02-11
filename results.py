import json
import cv2
import os

import utils

with open('results/bbox_genesis_2019_valid_results60000.json', 'r') as box:
    bboxes = json.load(box)

with open('results/genesis_valid_2019.json', 'r') as ann:
    annotations = json.load(ann)

with open('JsonUtils/10mostFrequentWords.json', 'r') as fw:
    frequentWordsDict = json.load(fw)

boundingBoxes = {}
numFound = 0
numNotFound = 0
numCompared = 0
numDetections = 0
numAnnotations = 0

for img in annotations['images']:
    image = cv2.imread('valid2019/{image_name}'.format(image_name=img['file_name']))
    image_id = int(img['file_name'].strip('.png')) + 188000  # Use it with 11 words
    #image_id = int(img['file_name'].strip('.png')) + 122000  # Use it with 20 words
    boundingBoxes[image_id] = {}
    boundingBoxes[image_id]['bboxes'] = []
    boundingBoxes[image_id]['annotations'] = []

    for el in bboxes:
        if el['image_id'] == image_id:
            cv2.rectangle(image, (int(el['bbox'][0]), int(el['bbox'][1])),
                      (int(el['bbox'][0] + el['bbox'][2]), int(el['bbox'][1] + el['bbox'][3])), (0, 255, 0),
                       thickness=1)
            cv2.putText(img=image, text=str(frequentWordsDict[el['category_id']]),
                        org=(int(el['bbox'][0]), int(el['bbox'][1]) - 5), fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=0.4, color=(0, 255, 0))
            boundingBoxes[image_id]['bboxes'].append(el['bbox'])
            numDetections += 1

    for x in annotations['annotations']:
        if x['image_id'] == image_id + 150:
            cv2.rectangle(image, (int(x['bbox'][0]), int(x['bbox'][1])),
                      (int(x['bbox'][0] + x['bbox'][2]), int(x['bbox'][1] + x['bbox'][3])), (0, 0, 255), thickness=1)
            cv2.putText(img=image, text=str(frequentWordsDict[x['category_id']]),
                        org=(int(x['bbox'][0]), int(x['bbox'][1]) + int(x['bbox'][3] + 5)),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(0, 0, 255))
            boundingBoxes[image_id]['annotations'].append(x['bbox'])
            numAnnotations += 1

    with open('bboxes.json', 'w+') as f:
        json.dump(boundingBoxes, f, indent=4)

    for box in boundingBoxes[image_id]['bboxes']:
        notes = []
        for ann in boundingBoxes[image_id]['annotations']:
            if (box[1] >= ann[1] - 20) and (box[1] <= ann[1] + 20):
                iou = utils.intersectionOverUnion(box, ann)
                if iou != 0.0 and ann not in notes:
                    if iou >= 0.5:
                        cv2.putText(img=image, text='Y',
                                    org=(int(box[0]), int(box[1]) + int(box[3] + 5)),
                                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255, 0, 0))
                        notes.append(ann)
                        numFound += 1
                        numCompared += 1
                        break
                    else:
                        cv2.putText(img=image, text='N',
                                    org=(int(box[0]), int(box[1]) + int(box[3] + 5)),
                                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255, 0, 0))
                        notes.append(ann)
                        numNotFound += 1
                        numCompared += 1
                        break

    if not os.path.exists('results'):
        os.mkdir('results')
    if not os.path.exists('results/comparisons_11_60000'):
        os.mkdir('results/comparisons_11_60000')
    cv2.imwrite('results/comparisons_11_60000/comp_{n}'.format(n=img['file_name']), image)

percentageFound = round((numFound / numCompared) * 100, 2)
percentageNotFound = round((numNotFound / numCompared) * 100, 2)
netCorrections = numDetections - numCompared
gTruthCorrections = numAnnotations - numCompared
accuracy = round((1 - (gTruthCorrections / numAnnotations)) * 100, 2)

print('numDetections: {x}'.format(x=numDetections))
print('numAnnotations: {x}'.format(x=numAnnotations))
print('numFound: {x}'.format(x=numFound))
print('numNotFound: {x}'.format(x=numNotFound))
print('numCompared: {x}'.format(x=numCompared))
print('percentage of found items: {x}%'.format(x=percentageFound))
print('percentage of not found items: {x}%'.format(x=percentageNotFound))
print('words found by the net but not shown in the ground truth: {x}'.format(x=netCorrections))
print('words shown in the ground truth but not found by the net: {x}'.format(x=gTruthCorrections))
print('net accuracy on given data is: {x}%'.format(x=accuracy))

analytics = {}
analytics['numDetections'] = numDetections
analytics['numAnnotations'] = numAnnotations
analytics['numFound'] = numFound
analytics['numNotFound'] = numNotFound
analytics['numCompared'] = numCompared
analytics['percentageFound'] = percentageFound
analytics['percentageNotFound'] = percentageNotFound
analytics['netCorrections'] = netCorrections
analytics['groundTruthCorrections'] = gTruthCorrections
analytics['accuracy'] = accuracy

with open('analytics/analytics_11_words_60000.json', 'w+') as f:
    json.dump(analytics, f, indent=4)


