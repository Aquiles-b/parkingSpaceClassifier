from typing import final
import cv2 as cv
import numpy as np
import math 

# Rotaciona uma imagem em @angle graus com o pivo no meio
def rotate_img(img, angle):
    xc, yc = img.shape[:2]
    mtx_rot = cv.getRotationMatrix2D((xc/2, yc/2), angle, 1)
    return cv.warpAffine(img, mtx_rot, (yc, xc))

# Rotaciona uma coordenada em @angle graus ao redor do @pivo
def rotate_coord(coord, angle, pivo):
    ar = math.radians(angle)
    x = coord[0] - pivo[0]
    y = coord[1] - pivo[1]
    xr, yr = (x*math.cos(ar) + y*math.sin(ar), -x*math.sin(ar) + y*math.cos(ar))
    xr = int(xr + pivo[0])
    yr = int(yr + pivo[1])
    return xr, yr

img = cv.imread('testeParking.jpg')
xc, yc = img.shape[:2]
# <center x="976" y="452" />
# <size w="46" h="65" />

w = 46
h = 65
x = 976 - w / 2
y = 452 - h / 2

img_rot = rotate_img(img, -7)
xi, yi = rotate_coord((x, y), -7, (xc/2, yc/2))

final_img = img_rot[yi:yi+h, xi:xi+w]

cv.imwrite('vamove.jpg', final_img)
