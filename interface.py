import tkinter as tk
from tkinter.messagebox import *

class application(tk.Tk):
    # Méthode d'initialisation de la fenêtre Tkinter
    def __init__(self):
        tk.Tk.__init__(self)
        self.size = 500
        self.creer_widgets()

    def creer_widgets(self):
        # Création canvas
        self.canv = tk.Canvas(self, bg="gray", height=250, width=100)
        self.canv.pack(side=tk.TOP)
        tk.Button(self, text="Bouton 1").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self, text="Bouton 2").pack(side=tk.RIGHT, padx=5, pady=5)

if __name__ == "__main__":
    app = application()
    app.title("Test interface")
    app.mainloop()