import cv2 as cv
import numpy as np

img = cv.imread('gradeNum.jpg')
rec = img[0:100, 0:100]
cv.imshow('teste', rec)
cv.waitKey(0)
