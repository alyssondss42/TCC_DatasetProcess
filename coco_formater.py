import os
import json
import random
import shutil
import cv2 as cv
from math import floor
from random import shuffle


def get_area(signature):
    bbox = signature['bounding_box']
    area = bbox['width'] * bbox['height']

    return area


def get_bbox(signature):
    bbox = signature['bounding_box']
    elements = [bbox['x'], bbox['y'], bbox['width'], bbox['height']]
    return elements


def split_data(file_path):
    random.seed(2)
    all_files = os.listdir(os.path.abspath(file_path))
    data_files = list(filter(lambda file: file.endswith('.json'), all_files))
    shuffle(data_files)

    split = 0.8
    split_index = floor(len(data_files) * split)
    training = data_files[:split_index]
    testing = data_files[split_index:]
    return training, testing


def copy_img(img_name, img_path, split_path):
    shutil.copy(os.path.join(img_path, img_name), os.path.join(split_path, img_name))


def create_gt(data, img_id, ann_id, image_list, annotation_list):
    img_name = data['img']
    img_width = data['img_width']
    img_height = data['img_height']
    sig_list = data['signatures']

    image_list.append(
        {
            'file_name': img_name,
            'height': img_height,
            'width': img_width,
            'id': img_id
        }
    )

    for sig in sig_list:
        annotation_list.append({
            'segmentation': [],
            'area': get_area(sig),
            'iscrowd': 0,
            'image_id': img_id,
            'bbox': get_bbox(sig),
            'category_id': 0,
            'id': ann_id
        })
        ann_id += 1

    return image_list, annotation_list, ann_id


# TODO: Implementar split train-val-test
def convert_2_coco(json_path):
    # Identificadores da imagem e da anotação
    img_id = 1
    ann_id = 1

    images_train = []
    annotations_train = []
    images_test = []
    annotations_test = []

    training, testing = split_data(json_path)

    for train_file in training:
        with open(os.path.join(json_path, train_file), 'r', encoding='utf-8') as file:
            data = json.load(file)

            images_train, annotations_train, ann_id = create_gt(data, img_id, ann_id,  image_list=images_train,
                                                                annotation_list=annotations_train)
            img_id += 1

            copy_img(img_name=data['img'], img_path=img_pth, split_path='output/coco/train/img')

    with open(os.path.join('output/coco/train/ann', 'train.json'), 'a', encoding='utf-8') as file:
        data = {
            'images': images_train,
            'annotations': annotations_train,
            'categories': [{'id': 0, 'name': 'signature'}]
        }
        json_obj = json.dumps(data, indent=4)
        file.write(json_obj)

    for test_file in testing:
        with open(os.path.join(json_path, test_file), 'r', encoding='utf-8') as file:
            data = json.load(file)

            images_test, annotations_test, ann_id = create_gt(data, img_id, ann_id, image_list=images_test,
                                                              annotation_list=annotations_test)
            img_id += 1

            copy_img(img_name=data['img'], img_path=img_pth, split_path='output/coco/test/img')

    with open(os.path.join('output/coco/test/ann', 'test.json'), 'a', encoding='utf-8') as file:
        data = {
            'images': images_test,
            'annotations': annotations_test,
            'categories': [{'id': 0, 'name': 'signature'}]
        }
        json_obj = json.dumps(data, indent=4)
        file.write(json_obj)


if __name__ == '__main__':
    img_pth = r'C:\Users\Alysson\Downloads\Poli-UPE-20211112T232533Z-001\Poli-UPE\10º Período\TCC\Dataset\Processed\Tobacco\img'
    json_pth = r'C:\Users\Alysson\Downloads\Poli-UPE-20211112T232533Z-001\Poli-UPE\10º Período\TCC\Dataset\Processed\Tobacco\json_gt'

    convert_2_coco(json_pth)

    print('ue')






