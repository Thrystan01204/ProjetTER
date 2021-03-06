import os
import sys
import time
import numpy as np
import tkinter
from cv2 import cv2


face_cascade=cv2.CascadeClassifier("C:/Users/Corentin/OneDrive/L3/Semestre2/EEEA/ProjetTER/haarcascade_fullbody.xml")#chemin absolu pour ce fichier
cap=cv2.VideoCapture("http://192.168.43.1:4747/video")#Adresse IP de la camera, pour tester, installer une applis qui transforme le tel en camera IP

#Reglage du nombre d'image par seconde
maximum_fps = 5 #une image sur maximum_fps sera affiché
counter = 0
#Reglage de la résolution du flux video
video_width= 1280
video_height= 720


while True:
    ret, frame=cap.read()
    if (counter % maximum_fps) == 0:
        frame = cv2.resize(frame, (video_width, video_height)) 
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

    counter += 1    
cap.release()
cv2.destroyAllWindows()
