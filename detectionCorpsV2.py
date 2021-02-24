import numpy as np
from cv2 import cv2
import tkinter as tk
from PIL import Image
from PIL import ImageTk

video_width= 256*2
video_height= 144*2


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 0, 255), thickness)

root = tk.Tk()

canvas = tk.Canvas(root)
canvas.grid(column=0, row=0)

frame = tk.Frame(root, bg="blue")
frame.grid(column=0, row=0)

conteneur = tk.LabelFrame(frame, bg="black")
conteneur.grid(column=0, row=0)

video = tk.Label(conteneur, bg="black")
video.grid(column=0, row=0)

cap = cv2.VideoCapture(0)


if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    cap=cv2.VideoCapture(0)
    while True:
        _,frame=cap.read()
        frame = cv2.resize(frame, (video_width, video_height)) 
        # tickmark=cv2.getTickCount()
        found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        draw_detections(frame,found)
        # fps=cv2.getTickFrequency()/(cv2.getTickCount()-tickmark)
        # cv2.putText(frame, "FPS: {:05.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        # ch = 0xFF & cv2.waitKey(1)
        # if ch == 27:
        #     break

        img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(img1))
        video['image'] = img
        root.update()
    # cv2.destroyAllWindows()