import os
import json
import shutil


def copy_json(json_path, json_name):
    dest_path = 'output/json_gt'
    shutil.copy(os.path.join(json_path, json_name), os.path.join(dest_path, json_name))


def copy_img(img_path, img_name):
    dest_path = 'output/img'
    shutil.copy(os.path.join(img_path, img_name), os.path.join(dest_path, img_name))


def create_json_gt(filename, width, height, signatures_zones, img_extension):
    json_path = 'output/json_gt'
    img_name = filename[:-3]+img_extension

    data = {
        'img': img_name,
        'img_width': width,
        'img_height': height,
        'count_sig': len(signatures_zones),
        'signatures': signatures_zones
    }

    json_filename = filename[:-3] + 'json'
    with open(os.path.join(json_path, json_filename), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

