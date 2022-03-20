import os
import json
import random
import cv2 as cv


def compute_scaling_factor(page_width, page_height, max_height, max_width):
    """
    Calcula o valor de resize.
    :param page_width: Largura da imagem.
    :param page_height: Altura da imagem.
    :param max_height: Altura máxima (default=640)
    :param max_width: Largura máxima (default=480)
    :return: Fator de resize.
    """
    scaling_factor = 1
    if max_height < page_height or max_width < page_width:
        scaling_factor = max_height / float(page_height)
        if max_width / float(page_width) < scaling_factor:
            scaling_factor = max_width / float(page_width)

    return scaling_factor


def resize_img(og_img, filename, factor, split_path):
    """
    Rescala imagem de acordo com o fator.
    :param split_path: train, test, val path
    :param og_img: Imagem em cv2.
    :param filename: Nome do arquivo.
    :param factor: Fator de resize.
    :return: Imagem rescalada e o nome do arquivo.
    """
    res_path = r'C:\Users\Alysson\PycharmProjects\TCC_DatasetProcess\output\yolo\images'
    res_path = res_path + '\\' + split_path

    res_img = cv.resize(og_img, None, fx=factor, fy=factor, interpolation=cv.INTER_AREA)
    jpg_filename = filename.split('.')[0] + '.jpg'
    cv.imwrite(os.path.join(res_path, jpg_filename), res_img)

    return res_img, jpg_filename


def get_points_scaled(signature_dict, factor):
    """
    Escalona os valore da bounding box da assinatura.
    :param signature_dict: Dicionário com as informações da assinatura.
    :param factor: Fator de resize.
    :return: x, y, w, h já escalados.
    """
    x = signature_dict['bounding_box']['x']
    y = signature_dict['bounding_box']['y']
    w = signature_dict['bounding_box']['width']
    h = signature_dict['bounding_box']['height']

    x_scaled = int(x * factor)
    y_scaled = int(y * factor)
    width_scaled = int(w * factor)
    height_scaled = int(h * factor)

    return x_scaled, y_scaled, width_scaled, height_scaled


def write_txt(filename, points, split_path):
    """
    Escreve arquivo .txt no padrão do YOLOV5.
    :param split_path: train, test, val
    :param filename: Nome da imagem em .jpg
    :param points: Ponto a serem adicionados no txt. Ordem: [x, y, w, h]
    :return: None
    """
    txt_path = r'C:\Users\Alysson\PycharmProjects\TCC_DatasetProcess\output\yolo\labels'
    txt_path = txt_path + '\\' + split_path
    txt_name = filename.split('.')[0]+'.txt'

    with open(os.path.join(txt_path, txt_name), 'a', encoding='utf-8') as txt_file:
        # Classe sempre '0' para afirmar que só precisamos identificar um objeto.
        gt_string = '0' + ' ' + str(round(points[0], 5)) + ' ' + str(round(points[1], 5)) + \
                    ' ' + str(round(points[2], 5)) + ' ' + str(round(points[3], 5))
        txt_file.write(gt_string)
        txt_file.write('\n')
        txt_file.close()


def split_dataset(list_files: list):
    random.seed()
    random.shuffle(list_files)

    cut_point = int(len(list_files)*0.8)
    train_files = list_files[:cut_point]
    remain_files = list_files[cut_point:]

    cut_point = int(len(remain_files)*0.5)
    val_files = remain_files[:cut_point]
    test_files = remain_files[cut_point:]

    return train_files, val_files, test_files


def get_partition(file_name, train, val, test):
    if file_name in train:
        split_type = 'train'
    elif file_name in val:
        split_type = 'val'
    else:
        split_type = 'test'

    return split_type


# TODO: Add split do dataset
def convert_2_yolo(json_path, img_path):
    """
    Main conversor.
    :param json_path: Path dos arquivos json no formato ALSS.
    :param img_path: Path das imagens.
    :return:
    """
    # Essas medidas são padrão do YOLO com COCO dataset.
    max_img_width = 960
    max_img_height = 1280

    for (root, dirnames, files) in os.walk(json_path):
        train_files, val_files, test_files = split_dataset(files)
        for filename in files:
            with open(os.path.join(root, filename), 'r', encoding='utf-8') as jfile:
                data = json.load(jfile)
                jfile.close()

            img_name = data['img']
            img_width = data['img_width']
            img_height = data['img_height']
            sig_list = data['signatures']

            orig_img = cv.imread(os.path.join(img_path, img_name))
            sc_factor = compute_scaling_factor(page_width=img_width, page_height=img_height,
                                               max_width=max_img_width, max_height=max_img_height)

            split_tp = get_partition(filename, train_files, val_files, test_files)
            res_img, new_img_name = resize_img(og_img=orig_img, filename=img_name, factor=sc_factor,
                                               split_path=split_tp)

            img_height_scaled, img_width_scaled = res_img.shape[:2]

            for sig in sig_list:
                x_scaled, y_scaled, w_scaled, h_scaled = get_points_scaled(signature_dict=sig, factor=sc_factor)

                x_center = int(x_scaled + (w_scaled/2))
                y_center = int(y_scaled + (h_scaled/2))

                x_center_norm = x_center/img_width_scaled
                y_center_norm = y_center/img_height_scaled
                w_norm = w_scaled/img_width_scaled
                h_norm = h_scaled/img_height_scaled

                write_txt(filename=new_img_name, points=[x_center_norm, y_center_norm, w_norm, h_norm],
                          split_path=split_tp)

            print('File {} to {} partition'.format(filename, split_tp))


if __name__ == '__main__':
    img_pth = r'C:\Users\Alysson\Downloads\tcc_dataset_v2\img'
    json_pth = r'C:\Users\Alysson\Downloads\tcc_dataset_v2\json_gt'

    convert_2_yolo(json_pth, img_pth)

    print('ue')