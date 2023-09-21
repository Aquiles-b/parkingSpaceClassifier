import cv2 as cv


# Retorna @img rotacionado em @angle graus em relacao ao meio da imagem.
def rotate_img(img, angle):
    height, width = img.shape[:2]
    mtx_rot = cv.getRotationMatrix2D((width/2, height/2), angle, 1)
    return cv.warpAffine(img, mtx_rot, (width, height))


# Retorna um recorte com a coordenada (x, y) no centro.
def get_img_rec(img, x, y, w, h):
    limits = img.shape[:2]
    wi = x - w
    hi = y - h
    wf = x + w
    hf = y + h
    xi = wi if wi >= 0 else 0
    yi = hi if hi >= 0 else 0
    xf = wf if wf <= limits[1] else limits[1]
    yf = hf if hf <= limits[0] else limits[0]

    return img[yi:yf, xi:xf]


# Retorna a vaga do estacionamento no ponto (x, y) com largura w e altura h, a
# imagem eh rotacionada em angle graus.
def crop_parking_space(img, x, y, w, h, angle):
    if angle <= -45:
        angle = 90 - abs(angle)
        aux = w
        w = h
        h = aux
    img_rec = get_img_rec(img, x, y, w, h)
    img_rot = rotate_img(img_rec, angle)
    y, x = img_rot.shape[:2]
    yi = round(y / 2 - h / 2)
    xi = round(x / 2 - w / 2)
    final_img = img_rot[yi:yi+h, xi:xi+w]
    return final_img
