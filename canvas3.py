from tkinter import *
import math
class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'white'
    SCREEN_W=1600
    SCREEN_H=1600



    def __init__(self):
        self.master = Tk()

        #self.line_button = Button(self.master, text='Line',command=self.set_tool_line)
        # self.line_button.grid(row=1,column=0)

        # self.circle_button = Button(self.master, text='Circle',command= self.set_tool_circle)
        # self.circle_button.grid(row=2,column=0)

        # self.point_button = Button(self.master, text='Point',command = self.set_tool_point)
        # self.point_button.grid(row=3,column=0)

        # self.point_button = Button(self.master, text='Freehand',command = self.set_tool_freehand)
        # self.point_button.grid(row=4,column=0)

        # self.point_button = Button(self.master, text ='Text', command = self.set_tool_text)
        # self.point_button.grid(row=5,column=0)
        self.scrollbarY = Scrollbar(self.master, orient = "vertical")
        self.scrollbarY.pack(side = RIGHT, fill = Y)
        self.draw_zone = Canvas(self.master,height=400,width=800,bg='gray11')
        self.draw_zone.pack(expand = True, fill = BOTH, anchor = E)
        self.scrollbarX = Scrollbar(self.master, orient = "horizontal")
        self.scrollbarX.pack(fill = BOTH)
        self.menubar = Menu(self.master)
        self.menu1 = Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Nouveau")
        self.menu1.add_command(label="Ouvrir")
        self.menu1.add_separator()
        self.menu1.add_command(label="Quitter", command=self.master.destroy)
        self.menubar.add_cascade(label="Fichier", menu=self.menu1)
        self.menu2 = Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Undo", command=self.undo )

        self.menu2.add_command(label="Redo")
        self.menubar.add_cascade(label="Editer", menu=self.menu2)

        #scrollbar
        self.draw_zone.configure(xscrollcommand = self.scrollbarX.set,
                                 yscrollcommand = self.scrollbarY.set,
                                 scrollregion = (0, 0, 10000, 5000))
        self.scrollbarX.configure(command = self.draw_zone.xview)
        self.scrollbarY.configure(command = self.draw_zone.yview)
        self.master.config(menu=self.menubar)
        self.master.title('Normal Mode')
        self.setup()
        self.master.mainloop()

    def setup(self):
        self.regZoom = 1
        self.line_start_x = None
        self.line_start_y = None

        self.circle_start_x = None
        self.circle_start_y = None

        self.text_start_x = None
        self.text_start_y = None


        self.Line_objects = []
        self.Point_objects = []
        self.stack = []
        self.redostack = []
        self.initialSizes = {}
        self.px = 0
        self.py = 0
        self.draw_zone.focus_set()
        self.recentText = None
        self.draw_zone.bind('<Button-1>', self.draw_start)
        self.draw_zone.bind('<B1-Motion>',self.draw_motion)
        self.draw_zone.bind('<ButtonRelease-1>',self.draw_end)
        self.draw_zone.bind("<Key>", self.change_text)
        self.draw_zone.bind("<MouseWheel>", self.zoomer)

        self.mode = ''


        #Text stuff
    def keyFun(self, event):
        pass
    def setMode(self, mode):
        self.mode = mode
        if mode == '':
            self.master.title("Normal Mode")
        if mode == 'text':
            self.master.title("Text Mode")
        if mode == 'textedit':
            self.master.title("Text Edit Mode")
        if mode == 'line':
            self.master.title("Line Mode")
        if mode == 'freehand':
            self.master.title("Freehand Mode")
        if mode == 'delete':
            self.master.title("Delete Mode")

    def line_start(self,event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        x = self.draw_zone.create_line(truex,truey,truex + 1,truey + 1,fill=self.DEFAULT_COLOR, width =
                                       5*self.regZoom)
        self.stack.append(x)
        self.initialSizes[x] = 5

    def line_motion(self,event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        x = self.stack[-1]
        curx = self.draw_zone.coords(x)[0]
        cury = self.draw_zone.coords(x)[1]
        self.draw_zone.coords(x, curx, cury, truex, truey)
    def line_end(self,event):
        pass


    def circle_start(self,event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.circle_start_x = truex
        self.circle_start_y = truey
    def circle_motion(self,event):
        self.draw_zone.delete('temp_circle_objects')   #sym de circle_end par rapport a circle_start
        self.draw_zone.create_oval((self.circle_start_x),(self.circle_start_y),truex,truey,fill=self.DEFAULT_COLOR,tags='temp_circle_objects')
    def circle_end(self,event):
        self.draw_zone.delete('temp_circle_objects')
        x=self.draw_zone.create_oval((self.circle_start_x),(self.circle_start_y),truex,truey,fill=self.DEFAULT_COLOR)
        self.stack.append(x)


    def point_start(self,event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        x = self.draw_zone.create_line(truex,truey,truex+1,truey+1)
        self.Point_objects.append(x)

#create line from this place to previous place

    def freehand_start(self, event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.px = truex
        self.py = truey
        self.stack.append("start")
    def freehand_motion(self, event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        x = self.draw_zone.create_line(self.px, self.py, truex, truey, fill=self.DEFAULT_COLOR, )
        self.px = truex
        self.py = truey
        self.stack.append(x)
        self.initialSizes[x] = 1
    def freehand_end(self, event):
        self.stack.append("end")


    def text_start(self, event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.text_start_x = truex
        self.text_start_y = truey
    def text_motion(self, event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)

        self.draw_zone.delete('temp_text_objects')
        fontsize = math.floor(0.8*(truey-self.text_start_y))
        if self.text_start_y > truey:
            self.draw_zone.create_text(self.text_start_x, truey, text = "\\\\", font = ("Purisa",round(fontsize)), tags = 'temp_text_objects', anchor = NW, fill = "white")
        elif self.text_start_y < truey:
            self.draw_zone.create_text(self.text_start_x, self.text_start_y, text = "\\\\", font = ("Purisa",round(fontsize)), tags = 'temp_text_objects', anchor = NW, fill = "white")
    def text_end(self, event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.draw_zone.delete('temp_text_objects')
        fontsize = math.floor(0.8*(truey-self.text_start_y))
        if self.text_start_y < truey:
            d = self.draw_zone.create_text(self.text_start_x, self.text_start_y, text = "\\\\", font =
                                       ("Purisa",round(fontsize)), anchor = NW, fill = "white")
        if self.text_start_y > truey:
            d = self.draw_zone.create_text(self.text_start_x, truey, text = "\\\\", font = ("Purisa",round(fontsize)), tags = 'temp_text_objects', anchor = NW, fill = "white")
        self.stack.append(d)
        self.initialSizes[d] = fontsize/self.regZoom

        self.setMode('textedit')


    def delete_motion(self, event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        inFreehand = False
        fhs = 0
        for i,x in enumerate(self.stack):
            if self.draw_zone.type(x) == 'text':
                size = self.initialSizes[x] * self.regZoom
                if (truex > self.draw_zone.coords(x)[0] and truex < size  + self.draw_zone.coords(x)[0] and
                truey > self.draw_zone.coords(x)[1] and truey < size + self.draw_zone.coords(x)[1]):
                    self.stack.remove(x)
                    self.draw_zone.delete(x)
            if x == 'start':
                inFreehand = True
                fhs = i
            if x == 'end':
                inFreehand = False
            if self.draw_zone.type(x) == 'line':
                x1 = self.draw_zone.coords(x)[0]
                x2 = self.draw_zone.coords(x)[2]
                y1 = self.draw_zone.coords(x)[1]
                y2 = self.draw_zone.coords(x)[3]
                distx = abs(x1-x2)
                disty = abs(y1-y2)
                #5*self.regZoom is consistent to viewport
                deldist = 5
                if ((abs(x1-truex) < deldist and abs(y1 - truey) < deldist) or
                        (abs(x2-truex) < deldist and abs(y2 - truey) < deldist)):
                    if inFreehand:
                        while self.stack[fhs] != 'end':
                            self.draw_zone.delete(self.stack[fhs])
                            self.stack.pop(fhs)
                    else:
                        self.stack.remove(x)
                        self.draw_zone.delete(x)



    def change_text(self, event):

        if event.keycode == 19:
            return
        c = event.char
        if c == '\x1b':
            if len(self.stack) > 0:
                top = self.stack[-1]
                if self.mode == 'textedit':
                    oldText = self.draw_zone.itemcget(top, 'text')
                    if oldText == '\\\\' or oldText == '\\':
                        oldText = ''
                    self.draw_zone.itemconfigure(top, text=oldText)
            self.setMode('')
            return
        if self.mode == 'textedit':
            top = self.stack[-1]
            oldText = self.draw_zone.itemcget(top, 'text')
            if c != '\x08' and event.keycode != 16:
                if oldText == '\\\\' or oldText == '\\':
                    oldText = ''
                newText = oldText + c
                self.draw_zone.itemconfigure(top, text=newText)
            if c == '\x7f':
                newText = oldText
                while True:
                    if c == '\r' or c == ' ':
                        newText = ''
                        break
                    if len(newText) == 0:
                        break
                    if newText[-1] == ' ':
                        break
                    if newText[-1] == '\r':
                        break
                    newText = newText[:-1]
                self.draw_zone.itemconfigure(top, text=newText)
            if c == '\x08':
                newText = oldText[:-1]
                if newText == '':
                    self.setMode('')
                self.draw_zone.itemconfigure(top, text=newText)
        if self.mode == '':
            if c == 'u':
                self.undo()
            if c == 'a':
                self.setMode('text')
            if c == 'o':
                self.setMode('freehand')
            if c == 'e':
                self.setMode('line')
            if c == ';':
                self.setMode('delete')
        if self.mode == 'line':
            if c == 'u':
                self.undo()
        if self.mode == 'freehand':
            if c == 'u':
                self.undo()




            # old = self.stack.pop()
            # self.draw_zone.delete(old)
            # #if delete
            # if event.char != '\x08':
                # d = self.draw_zone.create_text(self.topX, self.topY, text = self.topText + event.char, font = ("Purisa", self.topSize), anchor = NW)
                # self.topText = self.topText + event.char
                # self.stack.append(d)
            # else:
                # d = self.draw_zone.create_text(self.topX, self.topY, text = self.topText[:-1], font = ("Purisa", self.topSize), anchor = NW)
                # self.topText = self.topText[:-1]
                # self.stack.append(d)
        # self.draw_zone.delete(self.d)

    def set_tool_line(self):
        self.mode = ''
    def set_tool_circle(self):
        self.mode = ''
    def set_tool_point(self):
        self.mode = ''
    def set_tool_freehand(self):
        self.mode = ''
    def set_tool_text(self):
        self.mode = ''

    def draw_start(self,event):
        if self.mode =='line':
            self.line_start(event)
        elif self.mode == 'circle':
            self.circle_start(event)
        elif self.mode =='point':
            self.point_start(event)
        elif self.mode == "freehand":
            self.freehand_start(event)
        elif self.mode == 'text':
            self.text_start(event)

    def draw_motion(self,event):
        if self.mode =='line':
            self.line_motion(event)
        if self.mode == 'freehand':
            self.freehand_motion(event)
        elif self.mode == 'circle':
            self.circle_motion(event)
        elif self.mode == 'text':
            self.text_motion(event)
        elif self.mode == 'delete':
            
            self.delete_motion(event)


    def draw_end(self,event):
        if self.mode =='line':
            self.line_end(event)
        if self.mode =='freehand':
            self.freehand_end(event)
        elif self.mode == 'circle':
            self.circle_end(event)
        elif self.mode == 'text':
            self.text_end(event)

    def undo(self):
        x = self.stack.pop()
        if x == "end":
            while x != "start":
                x = self.stack.pop()
                self.draw_zone.delete(x)
        else:
            self.draw_zone.delete(x)
    def updateTopText(self, size, x, y):
        pass


    def zoomer(self, event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        #zoom in
        if event.delta > 0:
            self.draw_zone.scale("all", truex, truey, 1.1, 1.1)
            for x in self.stack:
                if self.draw_zone.type(x) == "text":
                    size = self.initialSizes[x] * self.regZoom
                    newsize = round((size*1.1))
                    #newX = self.draw_zone.itemconfigure(x, )
                    if newsize < 2:
                        newsize = 2
                    self.draw_zone.itemconfigure(x, font = ("Purisa", newsize))
                if self.draw_zone.type(x) == "line":
                    width = self.initialSizes[x] * self.regZoom
                    newwidth = round((width*1.1))
                    self.draw_zone.itemconfigure(x, width = newwidth)
            self.regZoom *= 1.1
        #zoom out
        elif (event.delta < 0):
            self.draw_zone.scale("all", truex, truey, 0.9, 0.9)
            for x in self.stack:
                if self.draw_zone.type(x) == "text":
                    size = self.initialSizes[x] * self.regZoom
                    newsize = round((size*0.9))
                    if newsize < 2:
                        newsize = 2
                    self.draw_zone.itemconfigure(x, font = ("Purisa", newsize))
                if self.draw_zone.type(x) == "line":
                    width = self.initialSizes[x] * self.regZoom
                    newwidth = round((width*0.9))
                    self.draw_zone.itemconfigure(x, width = newwidth)
            self.regZoom *= 0.9
if __name__ == '__main__':
    ge = Paint()
