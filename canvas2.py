from tkinter import ALL, EventType



canvas.bind("<MouseWheel>", do_zoom)
canvas.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

def do_zoom(event):
    factor = 1.001 ** event.delta
    canvas.scale(ALL, event.x, event.y, factor, factor)