import cv2 as cv
import os
import re
from crop_parking_space import crop_parking_space
import xml.etree.ElementTree as et


# Cria os diretorios necessarios para os recortes.
def create_dirs():
    empty_path = 'recs/empty'
    occupied_path = 'recs/occupied'
    if not os.path.exists(empty_path):
        os.makedirs(empty_path)
    if not os.path.exists(occupied_path):
        os.makedirs(occupied_path)


# Retorna um recorte em img de acordo com os dados em space.
def crop_space_xml(space, img):
    info_space = space.find('rotatedRect')
    coord_info = info_space.find('center')
    size_info = info_space.find('size')
    w = int(size_info.attrib['w'])
    h = int(size_info.attrib['h'])
    x = int(coord_info.attrib['x'])
    y = int(coord_info.attrib['y'])
    angle = int(info_space.find('angle').attrib['d'])

    return crop_parking_space(img, x, y, w, h, angle)


# Recorta todas as imagens de vagas registradas e as salva separando entre
# ocupada e vazia.
def segment_img(img_name, path_dest):
    img = cv.imread(img_name + ".jpg")
    tree = et.parse(img_name + ".xml")
    root = tree.getroot()
    spaces = root.findall('space')
    for s in spaces:
        id_space = s.attrib['id']
        space_rec = crop_space_xml(s, img)
        occupied = s.attrib['occupied']
        name = img_name + "#" + id_space + ".jpg"
        if (occupied == '1'):
            name = 'occupied/' + name
        else:
            name = 'empty/' + name
        name = 'recs/' + name
        try:
            cv.imwrite(name, space_rec)
        except:
            print('Nao foi possivel recortar a vaga', id_space)


def scans_files(path_files, segment_dir_path):
    img_re = r'.*\.jpg$'
    files = os.listdir(path_files)
    # Pega somente os .jpg
    imgs_jpg = [f for f in files if re.match(img_re, f)]
    # Remove extencao.
    imgs = [os.path.splitext(img)[0] for img in imgs_jpg]


def scans_dirs():
    pkLot_path = 'PKlot/PKlot'
    parkings = os.listdir(pkLot_path)
    pkLot_path += '/'
    for parking in parkings:
        wheaters = os.listdir(pkLot_path + parking)
        parking += '/'
        for wheater in wheaters:
            days = os.listdir(pkLot_path + parking + wheater)
            wheater += '/'
            for day in days:
                day += '/'
                segment_dir_path = 'PKLotSegmented/' + parking + wheater + day
                path_files = pkLot_path + parking + wheater + day
                scans_files(path_files, segment_dir_path)


if __name__ == '__main__':
    scans_dirs()
