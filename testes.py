import cv2 as cv
import numpy as np
import math

# <space id="85" occupied="1">
#     <center x="976" y="452" />
#     <size w="46" h="65" />
#     <angle d="-7" />
def rotaciona (x, y, angle, largura, altura):
    angulo_rotacao_radianos = math.radians(angle)
    x_rot = (x - largura) * math.cos(angulo_rotacao_radianos) - (y - altura) * math.sin(angulo_rotacao_radianos) + largura
    y_rot = (x - largura) * math.sin(angulo_rotacao_radianos) + (y - altura) * math.cos(angulo_rotacao_radianos) + altura
    return int(x_rot), int(y_rot)

angle = -7

img = cv.imread('teste.jpg')

# Obter o centro da imagem (ponto de rotação)
altura, largura = img.shape[:2]
centro = (largura // 2, altura // 2)
# Calcular a matriz de transformação de rotação
matriz_rotacao = cv.getRotationMatrix2D(centro, angle, 1.0)
# Aplicar a rotação à imagem
img_rot = cv.warpAffine(img, matriz_rotacao, (largura, altura))

w = 46
h = 65 
x = 976
y = 451

xn, yn = rotaciona(x, y, angle, largura, altura)

xi = xn - w // 4
yi = yn - h // 2
xf = xn + w
yf = yn + h

rec = img_rot[yi:yf, xi:xf]

cv.imshow("Recorte", rec)


cv.waitKey(0)
