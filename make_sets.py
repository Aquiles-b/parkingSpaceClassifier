import cv2 as cv
import numpy as np
from crop_parking_space import crop_parking_space
import xml.etree.ElementTree as et

arq_xml = '2012-09-12_06_20_57.xml'
img_name = '2012-09-12_06_20_57'
img = cv.imread(img_name + ".jpg")

tree = et.parse(arq_xml)
root = tree.getroot()

spaces = root.findall('space')

for s in spaces:
    id_space = s.attrib['id']
    occupied = s.attrib['occupied']
    info_space = s.find('rotatedRect')
    coord_info = info_space.find('center')
    size_info = info_space.find('size')
    w = int(size_info.attrib['w'])
    h = int(size_info.attrib['h'])
    x = int(coord_info.attrib['x'])
    y = int(coord_info.attrib['y'])
    angle = int(info_space.find('angle').attrib['d'])

    space_rec = crop_parking_space(img, x, y, w, h, angle)
    name = 'recs\\' + img_name + "#" + id_space + ".jpg"
    cv.imwrite(name, space_rec)
