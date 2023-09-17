import cv2 as cv
import numpy as np
from crop_parking_space import crop_parking_space
import xml.etree.ElementTree as et


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


arq_xml = '2012-09-12_07_34_01.xml'
img_name = '2012-09-12_07_34_01'
img = cv.imread(img_name + ".jpg")

tree = et.parse(arq_xml)
root = tree.getroot()
spaces = root.findall('space')

for s in spaces:
    space_rec = crop_space_xml(s)
    id_space = s.attrib['id']
    occupied = s.attrib['occupied']
    name = 'recs\\' + img_name + "#" + id_space + ".jpg"
    print(id_space, space_rec.shape)
    cv.imwrite(name, space_rec)
