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
def segment_img(img_path, img_name, path_dest):
    img = cv.imread(os.path.join(img_path, img_name + ".jpg"))
    tree = et.parse(os.path.join(img_path, img_name + ".xml"))
    root = tree.getroot()
    spaces = root.findall('space')
    for s in spaces:
        id_space = -1
        try:
            id_space = s.attrib['id']
            space_rec = crop_space_xml(s, img)
            occupied = s.attrib['occupied']
            name = img_name + "#" + id_space + ".jpg"
        except:
            print('Vaga id:', id_space, 'da imagem', img_name, 'faltando informacoes.')
            continue
        if (occupied == '1'):
            dir = 'occupied'
        else:
            dir = 'empty'
        name = os.path.join(path_dest, dir, name)
        try:
            cv.imwrite(name, space_rec)
        except:
            print('Nao foi possivel recortar a vaga', id_space)


def scans_files(path_files, segment_dir_path):
    if not os.path.exists(segment_dir_path):
        os.makedirs(segment_dir_path)
        os.makedirs(os.path.join(segment_dir_path, 'empty'))
        os.makedirs(os.path.join(segment_dir_path, 'occupied'))

    img_re = r'.*\.jpg$'
    files = os.listdir(path_files)
    # Pega somente os .jpg
    imgs_jpg = [f for f in files if re.match(img_re, f)]
    # Remove extencao.
    imgs = [os.path.splitext(img)[0] for img in imgs_jpg]
    # for img in imgs:
    segment_img(path_files, imgs[0], segment_dir_path)


def search_PKLot_dir():
    if not os.path.exists('PKLot'):
        print("PKLot nao encontrada.")
        exit(1)
    pkLot_path = 'PKLot'
    aux = os.path.join(pkLot_path, 'PKLot')
    if os.path.exists(aux):
        pkLot_path = aux

    return pkLot_path


def scans_dirs_PKLot():
    pkLot_path = search_PKLot_dir()
    parkings = os.listdir(pkLot_path)
    for parking in parkings:
        wheaters = os.listdir(os.path.join(pkLot_path, parking))
        for wheater in wheaters:
            days = os.listdir(os.path.join(pkLot_path, parking, wheater))
            isForTraining = True
            for day in days:
                if isForTraining:
                    segment_dir_path = os.path.join('PKLotSegmented', 'treino', parking, wheater, day)
                else:
                    segment_dir_path = os.path.join('PKLotSegmented', 'teste', parking, wheater, day)
                path_files = os.path.join(pkLot_path, parking, wheater, day)
                scans_files(path_files, segment_dir_path)
                isForTraining = not isForTraining


if __name__ == '__main__':
    scans_dirs_PKLot()
