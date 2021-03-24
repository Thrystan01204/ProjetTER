from __future__ import print_function
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2 as cv
import argparse
import numpy as np
import os
from datetime import datetime
import Filtre_KalmanOk

video_width= 1280
video_height= 720

Y=np.array([0,0,0,0])
fk=0
tours=0

#Chargement du fichier de sauvegarde

file_load = open("saves.txt", "r")

loads= file_load.readlines()
for i in loads:
    i= i.replace("\n", "")

#evenement bouton paramètres video et sauvegarde

def save():
    with open("saves.txt", "w") as filout:
        n= 0
        for i in loads:
            if n == 7:
                filout.write(str(i))
            else:
                filout.write(str(int(i)) +"\n")
            n = n + 1 

def addBlur():
    global kernel_blur
    global loads
    kernel_blur = min(43, kernel_blur+2)
    loads[0]= kernel_blur
    save()

def lessBlur():
    global kernel_blur
    global loads
    kernel_blur = max(1, kernel_blur-2)
    loads[0]= kernel_blur
    save()

def addSurface():
    global surface
    surface+=1000
    loads[2]= surface
    save()

def lessSurface():
    global surface
    surface = max(1000, surface-1000)
    loads[2]= surface
    save()

def addSeuil():
    global seuil
    seuil=min(255, seuil+1)
    loads[1]= seuil
    save()

def lessSeuil():
    global seuil
    seuil=max(1, seuil-1)
    loads[1]= seuil
    save()

#evenement bouton play/pause
playAction = True

def play():
    global playAction
    playAction = True

def pause():
    global playAction
    playAction = False

#Importation du flux video

cameraActived= False
cameraSourceWindow =None
cameraSource = loads[7]
prerempliChampCameraSource= None
def validCamera():
    global cameraSourceWindow
    global prerempliChampCameraSource
    global cameraSource
    global capture
    global cameraActived
    cameraSource = prerempliChampCameraSource.get()
    #http://10.244.22.128:4747/video
    capture.release()
    if cameraSource.isdigit():
        capture.open(int(cameraSource))
    else:
        capture.open(cameraSource)
    if capture.isOpened():
        cameraActived =True
    loads[7]= cameraSource
    save()
    cameraSourceWindow.destroy()

def importCamera():
    global cameraSourceWindow
    global cameraSource
    global prerempliChampCameraSource
    prerempliChampCameraSource= tk.StringVar()
    prerempliChampCameraSource.set(cameraSource)
    cameraSourceWindow = tk.Toplevel(root)
    champCamera = tk.Entry(cameraSourceWindow, textvariable= prerempliChampCameraSource, bg ="white", fg="black", width="50")
    champCamera.focus_set()
    champCamera.grid(row=0,column=0, padx = 5, pady = 5)
    valid = tk.Button(cameraSourceWindow, text="Valider et quitter", command=validCamera)
    valid.grid(column=0, row=1)

##Gestion de la zone de detection
newZone= False

def clicked(evt):
    global zoneX
    global zoneY
    global newZone
    global zoneW
    global zoneH
    if newZone:
        zoneW = evt.x - zoneX
        zoneH = evt.y - zoneY
        loads[3]= zoneX
        loads[4]= zoneY
        loads[5]= zoneW
        loads[6]= zoneH
        save()
        newZone = False
    else:
        zoneX = evt.x
        zoneY = evt.y
        zoneW = zoneX 
        zoneH = zoneY 
        newZone = True

def Move(evt):
    global zoneX
    global zoneY
    global newZone
    global zoneW
    global zoneH
    if newZone:
        zoneW = evt.x - zoneX
        zoneH = evt.y - zoneY        

kernel_blur=int(loads[0])
seuil=int(loads[1])
surface=int(loads[2])
zoneX= int(loads[3])
zoneY= int(loads[4])
zoneW= int(loads[5])
zoneH= int(loads[6])

file_load.close()

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
addKernelBlurBT.grid(column=1, row=1)

lessKernelBlurBT = tk.Button(root, text="Less blur", command=lessBlur)
lessKernelBlurBT.grid(column=1, row=2)

addSurfaceBT = tk.Button(root, text="add Surface", command=addSurface)
addSurfaceBT.grid(column=1, row=3)

lessSurfaceBT = tk.Button(root, text="less Surface", command=lessSurface)
lessSurfaceBT.grid(column=1, row=4)

addSurfaceBT = tk.Button(root, text="reduire bruit", command=addSeuil)
addSurfaceBT.grid(column=1, row=5)

lessSurfaceBT = tk.Button(root, text="ajouter bruit", command=lessSeuil)
lessSurfaceBT.grid(column=1, row=6)


# Vidéo
frame = tk.Frame(root, bg="blue")
frame.grid(column=0, row=1, rowspan= 7)
conteneur = tk.LabelFrame(frame, bg="black")
conteneur.grid(column=0, row= 1, rowspan= 7)
video = tk.Label(conteneur, bg="black")
video.grid(column=0, row=1, rowspan= 7)
video.bind("<Button-1>", clicked)
video.bind("<Motion>", Move)

#Menu
zoneMenu = tk.Frame(root, borderwidth=3)
zoneMenu.grid(row=0,column=0, columnspan=2)
menuSource = tk.Menubutton(zoneMenu, text='Source',borderwidth=2,relief = tk.RAISED)
menuSource.grid(row=0,column=0)

##Sous menu
menuDeroulant1 = tk.Menu(menuSource)

menuDeroulant1.add_command(label='Camera', command = importCamera)

menuSource.configure(menu=menuDeroulant1)

##Lecture video

playButton = tk.Button(root, text="PLay", command=play)
pauseButton = tk.Button(root, text="Pause", command=pause)

playButton.grid(column=0, row=8)
pauseButton.grid(column=0, row=9)

# [create]
#Creation d'un fond de masque d'image (méthodes principales d'instanciaton)

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
    
## [capture]
#On récupère le fichier vidéo et on le stoque dans une variable
capture = cv.VideoCapture(cameraSource)

if capture.isOpened():
    cameraActived =True

while True:

    if playAction: #Condition play/pause du flux video 
    #lit chaque séquence d'image de la vidéo jusqu'à se qu'il y en ait plus(break)
        ret, frame = capture.read()

    if frame is None:
        frame = np.zeros((int(video_height/2), int(video_width/2),3), np.uint8)
        cv.putText(frame, "No input video",(int(video_height/4), int(video_width/4)), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2) 
    ## [apply]
    #Met à jour le modele de masque de fond qu'on utilise (soustraction pixel)
    frame = cv.resize(frame, (video_width, video_height))
    fgMask = backSub.apply(frame)
    
    ## Détecte la personne qui fait une chute
    mask=cv.GaussianBlur(fgMask, (kernel_blur, kernel_blur), 0)
    mask=cv.threshold(mask, seuil, 255, cv.THRESH_BINARY)[1]
    mask=cv.dilate(mask, np.ones((5, 5), np.uint8), iterations=3)
    contours, nada=cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    frame_contour=frame.copy()

    DT=0.1
    tours=tours+1
    
    for c in contours:
        cv.drawContours(frame_contour, [c], 0, (0, 255, 0), 5)
        if cv.contourArea(c)<surface:
            continue
        
        x, y, w, h=cv.boundingRect(c)

        if tours==1:
            fk=Filtre_KalmanOk.Filtre_Kalman(x,y,w,h,DT,Y)
            (fk.X, fk.P) = fk.kf_predict()
        else:
            Y=np.array([x,y,w,h])
            fk.Y=Y
            (fk.X, fk.P, fk.K, fk.IM, fk.IS, fk.LH) = fk.kf_update(fk.X,fk.P, fk.Y, fk.H, fk.R)
            (fk.X, fk.P) = fk.kf_predict()
        print(fk.X,fk.P)
        
        if x>= zoneX and x <= zoneW and y>= zoneY and y <= zoneH :
            cv.rectangle(frame_contour, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv.imwrite("./screenshots/"+ str(datetime.now()).replace("_", "").replace(":", "-")+".png", frame)

    ## [display_frame_number]
    #création d' un rectangle qui va stocker l'image
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)

    ## [show]
    #affichage graphique de l'image de fond
    cv.putText(frame_contour, "[o|l]seuil: {:d}  [p|m]blur: {:d}  [i|k]surface: {:d}".format(seuil, kernel_blur, surface), (10, 30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
    cv.rectangle(frame_contour, (zoneX, zoneY), (zoneX+zoneW, zoneY+zoneH), (255, 0, 0), 2)

    img1 = cv.cvtColor(frame_contour, cv.COLOR_BGR2RGB)
    if playAction:
        cv.putText(img1, "play",(10, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
    else:
        cv.putText(img1, "pause",(10, 50),cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2)
    img = ImageTk.PhotoImage(Image.fromarray(img1))
    video['image'] = img
        
    root.update()
