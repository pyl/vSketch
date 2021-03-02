import tkinter as tk

def b1down(event):
    entry = tk.Entry(root,bd=0,font=("Purisa",60)) #No Border and added font:)
    entry.place(x= event.x, y= event.y)
    entry.focus_force()

root = tk.Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
drawing_area = tk.Canvas(root)
drawing_area.grid(sticky="N"+"E"+"S"+"W")
drawing_area.bind("<ButtonPress-1>", b1down)
root.mainloop()



drawing_area.bind("<MouseWheel>", do_zoom)
drawing_area.bind('<ButtonPress-1>', lambda event: drawing_area.scan_mark(event.x, event.y))
drawing_area.bind("<B1-Motion>", lambda event: drawing_area.scan_dragto(event.x, event.y, gain=1))

def do_zoom(event):
    factor = 1.001 ** event.delta
    drawing_area.scale(ALL, event.x, event.y, factor, factor)