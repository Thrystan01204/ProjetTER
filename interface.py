from __future__ import print_function
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2 as cv
import argparse
import numpy as np

def addBlur():
    global kernel_blur
    kernel_blur = min(43, kernel_blur+2)

def lessBlur():
    global kernel_blur
    kernel_blur = max(1, kernel_blur-2)

def addSurface():
    global surface
    surface+=1000

def lessSurface():
    global surface
    surface = max(1000, surface-1000)

def addSeuil():
    global seuil
    seuil=min(255, seuil+1)

def lessSeuil():
    global seuil
    seuil=max(1, seuil-1)

kernel_blur=5
seuil=15
surface=1000
zoneX= 150
zoneY= 150
zoneW= 300
zoneH= 300
width= 1280
height= 720


video_width= 256*2
video_height= 144*2

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                            OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
#argument 'input' qui contient le chemin d'accès à une vidéo ou séquences d'images

parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
#argument 'algo' qui définit le type de méthode pour la soustraction d'image (KNN, MOG2)

args = parser.parse_args()

root = tk.Tk()

# Boutons
addKernelBlurBT = tk.Button(root, text="Add blur", command=addBlur)
addKernelBlurBT.grid(column=0, row=0)

lessKernelBlurBT = tk.Button(root, text="Less blur", command=lessBlur)
lessKernelBlurBT.grid(column=1, row=0)

addSurfaceBT = tk.Button(root, text="add Surface", command=addSurface)
addSurfaceBT.grid(column=2, row=0)

lessSurfaceBT = tk.Button(root, text="less Surface", command=lessSurface)
lessSurfaceBT.grid(column=3, row=0)


# Vidéo
frame = tk.Frame(root, bg="blue")
frame.grid(column=0, row=1)
conteneur = tk.LabelFrame(frame, bg="black")
conteneur.grid(column=0, row=0)
video = tk.Label(conteneur, bg="black")
video.grid(column=0, row=0)

# [create]
#Creation d'un fond de masque d'image (méthodes principales d'instanciaton)

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
## [create]

## [capture]
#On récupère le fichier vidéo et on le stoque dans une variable
capture = cv.VideoCapture(0)
if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)


while True:
    #lit chaque séquence d'image de la vidéo jusqu'à se qu'il y en ait plus(break)
    ret, frame = capture.read()
    frame= cv.resize(frame, (1280, 720))
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
        if x>= zoneX and x <= zoneW and y>= zoneY and y <= zoneH :
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
    cv.rectangle(frame_contour, (zoneX, zoneY), (zoneX+zoneW, zoneY+zoneH), (255, 0, 0), 2)

    img1 = cv.cvtColor(frame_contour, cv.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img1))
    video['image'] = img

    root.update()
