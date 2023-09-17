import cv2 as cv
import math 

# Retorna @img rotacionado em @angle graus com o pivo no meio.
def rotate_img(img, angle):
    xc, yc = img.shape[:2]
    mtx_rot = cv.getRotationMatrix2D((xc/2, yc/2), angle, 1)
    return cv.warpAffine(img, mtx_rot, (yc, xc))

# Retorna a coordenada @coord rotacionada em @angle graus ao redor do @pivo.
def rotate_coord(coord, angle, pivo):
    ar = math.radians(angle)
    x = coord[0] - pivo[0]
    y = coord[1] - pivo[1]
    xr, yr = (x*math.cos(ar) + y*math.sin(ar), -x*math.sin(ar) + y*math.cos(ar))
    xr = int(xr + pivo[0])
    yr = int(yr + pivo[1])
    return xr, yr

# Retorna a vaga do estacionamento no ponto (x, y) com largura w e altura h, a
# imagem eh rotacionada em angle graus.
def crop_parking_space (img, x, y, w, h, angle):
    xc, yc = img.shape[:2]
    img_rot = rotate_img(img, angle)
    xi, yi = rotate_coord((x, y), angle, (xc/2, yc/2))
    xi = round(xi - w / 2)
    yi = round(yi - h / 2)
    final_img = img_rot[yi:yi+h, xi:xi+w]
    return final_img
