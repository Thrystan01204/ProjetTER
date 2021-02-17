import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, height=800, width=1000)
canvas.pack()

frame = tk.Frame(root, bg="blue")
frame.place(relheight=0.9, relwidth=1)

button = tk.Button(frame, text="Coucou", bg="white", fg="black", command=root.destroy)
button.pack(side=tk.LEFT)

root.mainloop()