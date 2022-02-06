import os
import json
import shutil
import xmltodict
import cv2 as cv


def draw_box_img(img_name, dl_zone):
    img = cv.imread(os.path.join('output/img', img_name))
    x_in = int(dl_zone['@col'])
    y_in = int(dl_zone['@row'])
    x_end = int(dl_zone['@width']) + x_in
    y_end = int(dl_zone['@height']) + y_in


def copy_img(img_name):
    img_path = r'C:\Users\Alysson\Downloads\Poli-UPE-20211112T232533Z-001\Poli-UPE\10º Período\TCC\Dataset\Full\tobacco_data_zhugy\Tobacco800_SinglePage\SinglePageTIF'
    dest_path = 'output/img'
    shutil.copy(os.path.join(img_path, img_name), os.path.join(dest_path, img_name))


def create_json_gt(filename, width, height, dl_zone):
    json_path = 'output/json_gt'
    signatures_zones = []

    if type(dl_zone) is list:
        for zone in dl_zone:
            signatures_zones.append({
                'bounding_box': {
                    'x': zone['@col'],
                    'y': zone['@row'],
                    'width': zone['@width'],
                    'height': zone['@height']
                }
            })
    else:  # É um dicionário.
        signatures_zones.append({
            'bounding_box': {
                'x': dl_zone['@col'],
                'y': dl_zone['@row'],
                'width': dl_zone['@width'],
                'height': dl_zone['@height']
            }
        })

    data = {
        'img': filename,
        'img_width': width,
        'img_height': height,
        'count_sig': len(signatures_zones),
        'signatures': signatures_zones
        }

    json_filename = filename[:-3] + 'json'
    with open(os.path.join(json_path, json_filename), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def preprocess_dataset(directory):
    for (dirpath, dirnames, files) in os.walk(directory):
        for filename in files:
            with open(os.path.join(dirpath, filename), 'r') as xml_file:
                data = xml_file.read()
                xml_file.close()

            try:
                file_dict = xmltodict.parse(data)

                dl_page = file_dict['GEDI']['DL_DOCUMENT']['DL_PAGE']
                img_name = dl_page['@src']
                width = dl_page['@width']
                height = dl_page['@height']

                if 'DL_ZONE' in dl_page.keys():
                    dl_zone = dl_page['DL_ZONE']
                    if type(dl_zone) is list:
                        signature_list = []
                        for zone in dl_zone:
                            area_type = zone['@gedi_type']
                            if area_type == 'DLSignature':
                                signature_list.append(zone)
                            else:
                                pass

                        create_json_gt(img_name, width, height, dl_zone=signature_list)
                        copy_img(img_name=img_name)

                    else:  # Somente um elemento
                        area_type = dl_zone['@gedi_type']

                        if area_type == 'DLSignature':
                            create_json_gt(img_name, width, height, dl_zone=dl_zone)
                            copy_img(img_name=img_name)
                        else:
                            pass
                else:  # Nao tem area de interesse
                    print('O arquivo ' + filename + ' nao tem area de interesse...')
            except Exception as exc:
                print('In file: ', filename)
                print(exc)


if __name__ == '__main__':
    path = r'C:\Users\Alysson\Downloads\Poli-UPE-20211112T232533Z-001\Poli-UPE\10º Período\TCC\Dataset\Full\tobacco_data_zhugy\Tobacc800_Groundtruth_v2.0\XMLGroundtruth_v2.0'
    preprocess_dataset(directory=path)