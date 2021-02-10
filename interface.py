import tkinter as tk

class application(tk.Tk):
    # Méthode d'initialisation de la fenêtre Tkinter
    def __init__(self):
        tk.Tk.__init__(self)
        self.size = 1000
        self.creer_widgets()

    def creer_widgets(self):
        # Création canvas
        self.canv = tk.Canvas(self, bg="light gray", height=self.size, width=self.size)
        self.canv.pack(side=tk.LEFT)

if __name__ == "__main__":
    app = application()
    app.title("Test interface")
    app.mainloop()