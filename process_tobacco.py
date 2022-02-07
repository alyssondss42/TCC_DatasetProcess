import os
import utils
import xmltodict
import cv2 as cv


def process_object_xml(zone):
    x_in = int(zone['@col'])
    y_in = int(zone['@row'])
    w = int(zone['@width'])
    h = int(zone['@height'])

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

                dl_page = file_dict['GEDI']['DL_DOCUMENT']['DL_PAGE']
                img_name = dl_page['@src']
                width = int(dl_page['@width'])
                height = int(dl_page['@height'])

                if 'DL_ZONE' in dl_page.keys():
                    dl_zone = dl_page['DL_ZONE']
                    if type(dl_zone) is list:
                        signature_list = []
                        for zone in dl_zone:
                            area_type = zone['@gedi_type']
                            if area_type == 'DLSignature':
                                signature_list.append(process_object_xml(zone=zone))
                            else:
                                pass

                        if len(signature_list) != 0:
                            utils.create_json_gt(filename, width, height, signatures_zones=signature_list,
                                                 img_extension='tif')
                            utils.copy_img(img_path=img_directory, img_name=img_name)

                    else:  # Somente um elemento
                        area_type = dl_zone['@gedi_type']
                        if area_type == 'DLSignature':
                            signature_list = [process_object_xml(dl_zone)]
                            utils.create_json_gt(filename, width, height, signatures_zones=signature_list,
                                                 img_extension='tif')
                            utils.copy_img(img_path=img_directory, img_name=img_name)
                        else:
                            pass
                else:  # Nao tem area de interesse
                    print('O arquivo ' + filename + ' nao tem area de interesse...')
            except Exception as exc:
                print('In file: ', filename)
                print(exc)


if __name__ == '__main__':
    path_xml = r'C:\Users\Alysson\Downloads\Poli-UPE-20211112T232533Z-001\Poli-UPE\10º Período\TCC\Dataset\Full\tobacco_data_zhugy\Tobacc800_Groundtruth_v2.0\XMLGroundtruth_v2.0'
    path_img = r'C:\Users\Alysson\Downloads\Poli-UPE-20211112T232533Z-001\Poli-UPE\10º Período\TCC\Dataset\Full\tobacco_data_zhugy\Tobacco800_SinglePage\SinglePageTIF'
    preprocess_dataset(xml_directory=path_xml, img_directory=path_img)