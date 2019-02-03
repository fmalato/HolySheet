import json
import os
import cv2

with open('results/bbox_genesis_2019_valid_results.json', 'r') as box:
    bboxes = json.load(box)

with open('results/genesis_valid_2019.json', 'r') as ann:
    annotations = json.load(ann)

with open('JsonUtils/10mostFrequentWords.json', 'r') as fw:
    frequentWordsDict = json.load(fw)


for img in annotations['images']:
    image = cv2.imread('valid2019/{image_name}'.format(image_name=img['file_name']))
    image_id = int(img['file_name'].strip('.png')) + 188000

    for el in bboxes:
        if el['image_id'] == image_id:
            cv2.rectangle(image, (int(el['bbox'][0]), int(el['bbox'][1])),
                      (int(el['bbox'][0] + el['bbox'][2]), int(el['bbox'][1] + el['bbox'][3])), (0, 255, 0), thickness=1)
            cv2.putText(img=image, text=str(frequentWordsDict[el['category_id']]),
                        org=(int(el['bbox'][0]), int(el['bbox'][1]) - 5), fontFace=cv2.FONT_HERSHEY_DUPLEX,
                        fontScale=0.4, color=(0, 255, 0))

    for x in annotations['annotations']:
        if x['image_id'] == image_id + 150:
            cv2.rectangle(image, (int(x['bbox'][0]), int(x['bbox'][1])),
                      (int(x['bbox'][0] + x['bbox'][2]), int(x['bbox'][1] + x['bbox'][3])), (0, 0, 255), thickness=1)
            cv2.putText(img=image, text=str(frequentWordsDict[x['category_id']]),
                        org=(int(x['bbox'][0]), int(x['bbox'][1]) + int(x['bbox'][3] + 5)),
                        fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(0, 0, 255))

    #cv2.imshow('{image}'.format(image=img['file_name']), image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    cv2.imwrite('results/comparisons/comp_{n}'.format(n=img['file_name']), image)

