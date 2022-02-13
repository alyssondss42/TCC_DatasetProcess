import os
import json


def get_bbox(signature):
    bbox = signature['bounding_box']
    elements = [bbox['x'], bbox['y'], bbox['width'], bbox['height']]
    return elements


# TODO: Implementar split train-val-test
def convert_2_coco(json_path):
    # Identificadores da imagem e da anotação
    img_id = 1
    ann_id = 1
    images = []
    annotations = []

    for (root, dirnames, files) in os.walk(json_path):
        for filename in files:
            with open(os.path.join(root, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)

            img_name = data['img']
            img_width = data['img_width']
            img_height = data['img_height']
            sig_list = data['signatures']

            images.append(
                {
                    'filename': img_name,
                    'height': img_height,
                    'width': img_width,
                    'id': img_id
                }
            )

            for sig in sig_list:
                annotations.append({
                    'segmentation': [],
                    'area': 1,
                    'iscrowd': 0,
                    'image_id': img_id,
                    'bbox': get_bbox(sig),
                    'category_id': 0,
                    'id': ann_id
                })
                ann_id += 1

            img_id += 1

    with open(os.path.join('output/coco', 'train.json'), 'a', encoding='utf-8') as file:
        data = {
            'images': images,
            'annotations': annotations,
            'categories': [{'id': 0, 'name': 'signature'}]
        }
        json_obj = json.dumps(data, indent=4)
        file.write(json_obj)


if __name__ == '__main__':
    img_pth = r'C:\Users\Alysson\Downloads\test_yolor\img'
    json_pth = r'C:\Users\Alysson\Downloads\test_yolor\json'

    convert_2_coco(json_pth)

    print('ue')






