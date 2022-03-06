import os
import json
import cv2 as cv


def resize_img(orig_img, img_name, max_height=640, max_width=480):
    page_height, page_width, _ = orig_img.shape

    scaling_factor = 1
    if max_height < page_height or max_width < page_width:
        scaling_factor = max_height / float(page_height)
        if max_width / float(page_width) < scaling_factor:
            scaling_factor = max_width / float(page_width)

    res_img = cv.resize(orig_img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv.INTER_AREA)
    cv.imwrite(os.path.join('./output/vgg_alss/img_res', img_name), res_img)


def read_vgg_ann_file(directory):
    with open(directory, 'r', encoding='utf-8') as vgg_file:
        data = json.load(vgg_file)
        vgg_file.close()

    return data


def create_alss_json_gt(img_name, img_w, img_h, c_sig, sig_list):
    json_filename = img_name.split('.')[0] + '.json'
    with open(os.path.join('./output/vgg_alss/json', json_filename), 'w', encoding='utf-8') as alss_file:
        data = {
            'img': img_name,
            'img_width': img_w,
            'img_height': img_h,
            'count_sig': c_sig,
            'signatures': sig_list
        }
        json_obj = json.dumps(data, indent=4)
        alss_file.write(json_obj)


def prepare_dataset(image_path, vgg_path):
    json_vgg_file = read_vgg_ann_file(directory=vgg_path)

    for (root, dirnames, files) in os.walk(image_path):
        for filename in files:
            if filename.endswith('.png') or filename.endswith('.PNG'):
                img = cv.imread(os.path.join(root, filename))
                img_h, img_w, _ = img.shape
                sig_list = []
                count_sig = 0

                img_infos = [v for k, v in json_vgg_file.items() if k.startswith(filename)]

                for current_img in img_infos:
                    regions = current_img['regions']
                    count_sig = len(regions)

                    for reg in regions:
                        shape_attr = reg['shape_attributes']
                        sig_list.append({
                            'bounding_box': {
                                'x': shape_attr['x'],
                                'y': shape_attr['y'],
                                'width': shape_attr['width'],
                                'height': shape_attr['height']
                            }
                        })

                    create_alss_json_gt(img_name=filename, img_w=img_w, img_h=img_h, c_sig=count_sig, sig_list=sig_list)
                    resize_img(orig_img=img, img_name=filename)


if __name__ == '__main__':
    image_pth = r'C:\Users\Alysson\Downloads\Xerox_dataset\assinados'
    json_dir = r'C:\Users\Alysson\Downloads\Xerox_dataset\tcc_dataset_test_json.json'

    prepare_dataset(image_path=image_pth, vgg_path=json_dir)






