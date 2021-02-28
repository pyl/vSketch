import tkinter as tk

def b1down(event):
    entry = tk.Entry(root,bd=0,font=("Purisa",15)) #No Border and added font:)
    entry.place(x= event.x, y= event.y)
    entry.focus_force()

root = tk.Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
drawing_area = tk.Canvas(root)
drawing_area.grid(sticky="N"+"E"+"S"+"W")
drawing_area.bind("<ButtonPress-1>", b1down)
root.mainloop()