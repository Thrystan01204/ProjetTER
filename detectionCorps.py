import os
import sys
import time
import numpy as np
import tkinter
from cv2 import cv2


face_cascade=cv2.CascadeClassifier("C:/Users/Corentin/OneDrive/L3/Semestre2/EEEA/ProjetTER/haarcascade_fullbody.xml")#chemin absolu pour ce fichier
cap=cv2.VideoCapture("http://192.168.43.1:4747/video")#Adresse IP de la camera, pour tester, installer une applis qui transforme le tel en camera IP

while True:
    ret, frame=cap.read()
    frame = cv2.resize(frame, (256, 144)) 
    tickmark=cv2.getTickCount()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face=face_cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
    fps=cv2.getTickFrequency()/(cv2.getTickCount()-tickmark)
    cv2.putText(frame, "FPS: {:05.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow('video', frame)
cap.release()
cv2.destroyAllWindows()