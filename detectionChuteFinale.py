from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np


kernel_blur=5
seuil=15
surface=1000


#programme d'extraction de fond d'image:
#(méthode de soustraction des valeurs pixels en valeurs absolues)


#on ajoute différents arguments d'entrée à la ligne de commande pour
#le traitement du flux vidéo

originale = cv.imread('./teset.png',0)

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
#argument 'input' qui contient le chemin d'accès à une vidéo ou séquences d'images

parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
#argument 'algo' qui définit le type de méthode pour la soustraction d'image (KNN, MOG2)

args = parser.parse_args()


# [create]
#Creation d'un fond de masque d'image (méthodes principales d'instanciaton)

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
## [create]

## [capture]
#On récupère le fichier vidéo et on le stoque dans une variable
capture = cv.VideoCapture("http://192.168.137.199:4747/video")
if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)


#boucle qui v lire chaque image vidéo
while True:
    #lit chaque séquence d'image de la vidéo jusqu'à se qu'il y en ait plus(break)
    ret, frame = capture.read()
    if frame is None:
        break
    ## [apply]
    #Met à jour le modele de masque de fond qu'on utilise (soustraction pixel)
    fgMask = backSub.apply(frame)
    
    ## Détecte la personne qui fait une chute
    mask=cv.GaussianBlur(fgMask, (kernel_blur, kernel_blur), 0)
    mask=cv.threshold(mask, seuil, 255, cv.THRESH_BINARY)[1]
    mask=cv.dilate(mask, np.ones((5, 5), np.uint8), iterations=3)
    contours, nada=cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    frame_contour=frame.copy()
    for c in contours:
        cv.drawContours(frame_contour, [c], 0, (0, 255, 0), 5)
        if cv.contourArea(c)<surface:
            continue
        x, y, w, h=cv.boundingRect(c)
        cv.rectangle(frame_contour, (x, y), (x+w, y+h), (0, 0, 255), 2)

    ## [display_frame_number]
    #création d' un rectangle qui va stocker l'image
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    #ajout du numéro de la séquence d'image dans notre rectangle
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    

    ## [show]
    #affichage graphique de l'image de fond
    cv.putText(frame_contour, "[o|l]seuil: {:d}  [p|m]blur: {:d}  [i|k]surface: {:d}".format(seuil, kernel_blur, surface), (10, 30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
    cv.imshow("contour", frame_contour)
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
   
    #touche 'q' => fin de l'affichage
    key=cv.waitKey(30)&0xFF
    if key==ord('q'):
        break
    if key==ord('p'):
        kernel_blur=min(43, kernel_blur+2)
    if key==ord('m'):
        kernel_blur=max(1, kernel_blur-2)
    if key==ord('i'):
        surface+=1000
    if key==ord('k'):
        surface=max(1000, surface-1000)
    if key==ord('o'):
        seuil=min(255, seuil+1)
    if key==ord('l'):
        seuil=max(1, seuil-1)
    if key==ord('l'):
        seuil=max(1, seuil-1)
