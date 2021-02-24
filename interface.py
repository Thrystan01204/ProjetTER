import tkinter as tk
from PIL import Image
from PIL import ImageTk
from cv2 import cv2

# root = tk.Tk()

# canvas = tk.Canvas(root, height=800, width=1000)
# canvas.pack()

# frame = tk.Frame(root, bg="blue")
# frame.place(relheight=0.1, relwidth=1)

# button = tk.Button(frame, text="Coucou", bg="white", fg="black", command=root.destroy)
# button.pack(side=tk.TOP)

# conteneur = tk.LabelFrame(frame, bg="black")
# conteneur.pack()

# video = tk.Label(conteneur, bg="black")
# video.pack()

# cap = cv2.VideoCapture(0)

# while True:
#     img = cap.read()[1]
#     img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = ImageTk.PhotoImage(Image.fromarray(img1))
#     video['image'] = img
#     root.update()

class Interface(tk.Tk):
    def __init__(self, parent=None, webcam=0):
        tk.Tk.__init__(self, parent)
        self.webcam = webcam
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        #self.canvas = tk.Canvas(height=800, width=1500)
        self.frame = tk.Frame(self.parent, bg="blue")
        self.frame.grid(column=0, row=0)

        self.conteneur = tk.LabelFrame(self.frame, bg="black")
        self.conteneur.grid(column=0, row=0)

        self.video = tk.Label(self.conteneur, bg="black")
        self.video.grid(column=0, row=1)

        self.cap = cv2.VideoCapture(self.webcam)

    def update_video(self):
        self.img = self.cap.read()[1]
        self.img1 = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = ImageTk.PhotoImage(Image.fromarray(self.img1))

        self.video['image'] = self.img
        self.update()

    def get_webcam(self):
        return self.webcam


app = Interface()
app.title('Test')

while True:
    app.update_video()