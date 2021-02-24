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
        self.frame = tk.Frame(self.parent, bg="blue")
        self.frame.grid(colum=0, row=1)

        self.button = tk.Button(text=('Test button'))
        self.button.grid(column=1, row=0)

        self.conteneur = tk.LabelFrame(self.frame, bg="black")
        self.conteneur.grid(column=0, row=0)

        self.video = tk.Label(self.conteneur, bg="black")
        self.video.grid(column=0, row=0)

        self.cap = cv2.VideoCapture(self.webcam)

    def update_video(self):
        self.img = self.cap.read()[1]
        self.img1 = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = ImageTk.PhotoImage(Image.fromarray(self.img1))

        self.video['image'] = self.img
        self.update()

    def get_webcam(self):
        return self.webcam


class OpenCV(cv2):
    def __init__(self, webcam) -> None:
        super().__init__()
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    def draw_detections(self, img, rects, thickness = 1):
        for x, y, w, h in rects:
            # the HOG detector returns slightly larger rectangles than the real objects.
            # so we slightly shrink the rectangles to get a nicer output.
            self.pad_w, self.pad_h = int(0.15*w), int(0.05*h)
            cv2.rectangle(img, (x+self.pad_w, y+self.pad_h), (x+w-self.pad_w, y+h-self.pad_h), (0, 0, 255), thickness)
    
    def update_detection(self):
        return 0



app = Interface()
app.title('Test')

while True:
    app.update_video()