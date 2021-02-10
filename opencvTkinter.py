from cv2 import cv2
import numpy as np

cap = cv2.VideoCapture(2)

img1 = cap.read()[1]

print(img1.shape)