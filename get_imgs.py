import os
import json
import utils
import uuid


def get_files_partitions(txt_path, img_path, json_path):
    """
    Pega os arquivos de acordo com o diretorio da particao passada no txt_path.

    :param txt_path: Path dos arquivos txt no formato yolo
    :param img_path: Path das imagens originais
    :param json_path: Path dos json no formato alss
    :return:
    """
    for (root, dirnames, files) in os.walk(txt_path):
        for filename in files:
            json_name = filename.replace('.txt', '.json')

            with open(os.path.join(json_path, json_name), 'r', encoding='utf-8') as jfile:
                data = json.load(jfile)
                jfile.close()

            img_name = data['img']

            utils.copy_img(img_path, img_name)
            utils.copy_json(json_path, json_name)


def copy_imgs(json_path, img_path):
    for (root, dirnames, files) in os.walk(json_path):
        for filename in files:
            with open(os.path.join(root, filename), 'r', encoding='utf-8') as jfile:
                data = json.load(jfile)
                jfile.close()

            img_name = data['img']

            utils.copy_img(img_path, img_name)


def get_img_in_folders(img_path):
    for (root, dirnames, files) in os.walk(img_path):
        for filename in files:
            utils.copy_img(root, filename)


def count_img(path_img):
    count = 0
    for (root, dirnames, files) in os.walk(path_img):
        for filename in files:
            if filename.endswith('_preProcess.png'):
                count += 1

    return count



if __name__ == '__main__':
    # j_path = r'C:\Users\Alysson\Downloads\TCC_dataset_xerox\Lote9\json_alss'
    # i_path = r'C:\Users\Alysson\Downloads\TCC_dataset_xerox\Lote9\img'
    # copy_imgs(json_path=j_path, img_path=i_path)

    # i_path = r'C:\Users\Alysson\Downloads\tcc_dataset_v2\img'
    # j_path = r'C:\Users\Alysson\Downloads\tcc_dataset_v2\json_gt'
    # t_path = r'C:\Users\Alysson\PycharmProjects\TCC_DatasetProcess\output\yolo\labels\train'
    #
    # get_files_partitions(txt_path=t_path, img_path=i_path, json_path=j_path)

    # i_path = r'C:\Users\Alysson\Downloads\TCC_dataset_xerox\LoteID\yolo\detection_'
    # get_img_in_folders(img_path=i_path)

    i_path = r'C:\Users\Alysson\Downloads\tcc_dataset_v2\img'
    print(count_img(path_img=i_path))