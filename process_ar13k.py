import os
import json
import utils
import shutil
import xmltodict
import cv2 as cv


def process_object_xml(obj):
    bb = obj['bndbox']
    x_in = int(bb['xmin'])
    y_in = int(bb['ymin'])
    w = int(bb['xmax']) - x_in
    h = int(bb['ymax']) - y_in

    return {
        'bounding_box': {
            'x': x_in,
            'y': y_in,
            'width': w,
            'height': h
        }
    }


def preprocess_dataset(xml_directory, img_directory):
    for (dirpath, dirnames, files) in os.walk(xml_directory):
        for filename in files:
            with open(os.path.join(dirpath, filename), 'r') as xml_file:
                data = xml_file.read()
                xml_file.close()

            try:
                file_dict = xmltodict.parse(data)
                annotation = file_dict['annotation']

                img_width = int(annotation['size']['width'])
                img_height = int(annotation['size']['height'])
                img_name = filename[:-3]+'jpg'
                objects = annotation['object']

                if type(objects) is list:
                    signature_list = []
                    for obj in objects:
                        if obj['name'] == 'signature':
                            signature_list.append(process_object_xml(obj))
                        else:
                            pass

                    if len(signature_list) != 0:
                        utils.create_json_gt(filename, img_width, img_height, signatures_zones=signature_list,
                                             img_extension='jpg')
                        # utils.copy_img(img_path=img_directory, img_name=img_name)
                else:
                    if objects['name'] == 'signature':
                        signature_list = [process_object_xml(objects)]

                        utils.create_json_gt(img_name, img_width, img_height, signatures_zones=signature_list,
                                             img_extension='jpg')
                        # utils.copy_img(img_path=img_directory, img_name=img_name)

            except Exception as exc:
                print('In file: ', filename)
                print(exc)


if __name__ == '__main__':
    path_xml = r'C:\Users\Alysson\Downloads\Poli-UPE-20211112T232533Z-001\Poli-UPE\10º Período\TCC\Dataset\Full\AR_13K_dataset\validation_xml\validation_xml'
    path_img = r'C:\Users\Alysson\Downloads\Poli-UPE-20211112T232533Z-001\Poli-UPE\10º Período\TCC\Dataset\Full\AR_13K_dataset\validation_images\validation_images'
    preprocess_dataset(xml_directory=path_xml, img_directory=path_img)

