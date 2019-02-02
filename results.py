# TODO: aprire il file con le annotations e quello con i risultati, disegnare un rettangolo rosso per ogni elemento
#       delle annotations, verde per ogni result. Confrontarli e trovare le statistiche utili.

import json
import os
import cv2

with open('results/bbox_genesis_2019_valid_results.json', 'r') as box:
    bboxes = json.load(box)

with open('results/genesis_valid_2019.json', 'r') as ann:
    annotations = json.load(ann)

for img in annotations['images']:
    image = cv2.imread('valid2019/{image_name}'.format(image_name=img['file_name']))
    image_id = int(img['file_name'].strip('.png')) + 188000
    for el in bboxes:
        if el['image_id'] == image_id:
            cv2.rectangle(image, (int(el['bbox'][0]), int(el['bbox'][1])),
                      (int(el['bbox'][0] + el['bbox'][2]), int(el['bbox'][1] + el['bbox'][3])), (0, 255, 0), thickness=2)
    for x in annotations['annotations']:
        if x['image_id'] == image_id+150:
            cv2.rectangle(image, (int(x['bbox'][0]), int(x['bbox'][1])),
                      (int(x['bbox'][0] + x['bbox'][2]), int(x['bbox'][1] + x['bbox'][3])), (0, 0, 255), thickness=1)

    cv2.imshow('{image}'.format(image=img['file_name']), image)
    cv2.waitKey(100000)
    cv2.destroyAllWindows()

