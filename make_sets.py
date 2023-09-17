import cv2 as cv
import os
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


def crop_space_xml(space):
    info_space = space.find('rotatedRect')
    coord_info = info_space.find('center')
    size_info = info_space.find('size')
    w = int(size_info.attrib['w'])
    h = int(size_info.attrib['h'])
    x = int(coord_info.attrib['x'])
    y = int(coord_info.attrib['y'])
    angle = int(info_space.find('angle').attrib['d'])

    return crop_parking_space(img, x, y, w, h, angle)


img_name = '2012-09-12_10_11_12'
img = cv.imread(img_name + ".jpg")

tree = et.parse(img_name + ".xml")
root = tree.getroot()
spaces = root.findall('space')

for s in spaces:
    create_dirs()
    id_space = s.attrib['id']
    space_rec = crop_space_xml(s)
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
