import cv2 as cv
import numpy as np
from skimage import feature
import csv

img = cv.imread('PKLotSegmented/PUCPR/Cloudy/2012-09-12/occupied/2012-09-12_07_54_56#1.jpg')
if img is None:
    print('Deu ruim')
    exit(1)

imgC = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
lbp = feature.local_binary_pattern(imgC, 8, 3, method='nri_uniform')
hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 60), range=(0, 255))

print(hist)
cv.imshow('lbp', lbp)
cv.waitKey(0)
