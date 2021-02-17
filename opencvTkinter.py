from cv2 import cv2
import numpy as np
from tkinter import * 
from PIL import Image
from PIL import ImageTk


root = Tk()
root.geometry("700x540")
root.configure(bg="black")
Label(root, text="Ma Cam", font=("times new roman", 30, "bold"), bg="black", fg="red").pack()
f1 = LabelFrame(root, bg="red")
f1.pack()
L1 = Label(f1, bg="red")
L1.pack()
cap = cv2.VideoCapture(0)

while True:
    img = cap.read()[1]
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(img1))
    L1['image'] = img
    root.update()