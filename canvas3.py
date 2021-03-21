from tkinter import *
import math
class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
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
        self.draw_zone = Canvas(self.master,height=400,width=400,bg='white')
        self.draw_zone.pack(expand = True, fill = BOTH)
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
        self.draw_zone.configure(xscrollcommand = self.scrollbarX.set, scrollregion = (0, 0, 10000, 1000))
        self.scrollbarX.configure(command = self.draw_zone.xview)

        # self.scrollbarX.grid(row = 1, column = 0, sticky = "ew")
        # self.draw_zone.grid(row = 0, column = 0, sticky = "nsew")


        self.master.config(menu=self.menubar)
        self.master.title('UI')

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


        self.modeText = self.draw_zone.create_text(5, 5, text = "Normal Mode", anchor = 'nw')


        #Text stuff

    def keyFun(self, event):
        pass
    def setMode(self, mode):
        self.mode = mode
        if mode == '':
            self.draw_zone.itemconfigure(self.modeText, text='Normal Mode')
        if mode == 'text':
            self.draw_zone.itemconfigure(self.modeText, text='Text Mode')
        if mode == 'textedit':
            self.draw_zone.itemconfigure(self.modeText, text='Text Edit Mode')
        if mode == 'line':
            self.draw_zone.itemconfigure(self.modeText, text='Line Mode')
        if mode == 'freehand':
            self.draw_zone.itemconfigure(self.modeText, text='Freehand Mode')




    def line_start(self,event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.line_start_x=truex
        self.line_start_y=truey
    def line_motion(self,event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.draw_zone.delete('temp_line_objects')
        self.draw_zone.create_line(self.line_start_x,self.line_start_y,truex,truey,fill=self.DEFAULT_COLOR,smooth=1,tags='temp_line_objects', width = 10)
    def line_end(self,event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.draw_zone.delete('temp_line_objects')
        x=self.draw_zone.create_line(self.line_start_x,self.line_start_y,truex,truey,fill=self.DEFAULT_COLOR,smooth=1, width = 10)
        self.Line_objects.append(x)
        self.stack.append(x)


    def circle_start(self,event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.circle_start_x = truex
        self.circle_start_y = truey
    def circle_motion(self,event):
        self.draw_zone.delete('temp_circle_objects')   #sym de circle_end par rapport a circle_start
        #self.draw_zone.create_oval(event.x,event.y,(2*self.circle_start_x-event.x),(2*self.circle_start_y-event.y),tags='temp_circle_objects')
        self.draw_zone.create_oval((self.circle_start_x),(self.circle_start_y),truex,truey,fill=self.DEFAULT_COLOR,tags='temp_circle_objects')
    def circle_end(self,event):
        self.draw_zone.delete('temp_circle_objects')
        #x=self.draw_zone.create_oval(event.x,event.y,(2*self.circle_start_x-event.x),(2*self.circle_start_y-event.y))
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
        x = self.draw_zone.create_line(self.px, self.py, truex, truey, fill=self.DEFAULT_COLOR,smooth=1)
        self.px = truex
        self.py = truey
        self.stack.append(x)
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
        self.draw_zone.create_text(self.text_start_x, self.text_start_y, text = "hello", font = ("Purisa",
                                                                                                 math.floor(0.8*(truey-self.text_start_y))), tags = 'temp_text_objects', anchor = NW)
    def text_end(self, event):
        truex = self.draw_zone.canvasx(event.x)
        truey = self.draw_zone.canvasy(event.y)
        self.draw_zone.delete('temp_text_objects')
        fontsize = math.floor(0.8*(truey-self.text_start_y))
        d = self.draw_zone.create_text(self.text_start_x, self.text_start_y, text = "hello", font = ("Purisa",fontsize), anchor = NW)
        self.stack.append(d)
        self.initialSizes[d] = fontsize

        self.setMode('textedit')
    def change_text(self, event):
        c = event.char
        if c == '\x1b':
            self.setMode('')
            return
        if self.mode == 'textedit':
            top = self.stack[-1]
            oldText = self.draw_zone.itemcget(top, 'text')
            if c != '\x08':
                newText = oldText + c
                self.draw_zone.itemconfigure(top, text=newText)
            if c == '\x08':
                newText = oldText[:-1]
                self.draw_zone.itemconfigure(top, text=newText)
        if self.mode == '':
            if c == 'a':
                self.setMode('text')
            if c == 'o':
                self.setMode('freehand')
            if c == 'e':
                self.setMode('line')




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
        self.setMode('')
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
            self.regZoom *= 1.1
            for x in self.stack:
                if self.draw_zone.type(x) == "text":
                    size = int(self.draw_zone.itemcget(x, 'font')[7:])
                    if size < 2:
                        size = 2
                    newsize = math.ceil((size*1.1)+1)
                    #newX = self.draw_zone.itemconfigure(x, )
                    self.draw_zone.itemconfigure(x, font = ("Purisa", newsize))
                if self.draw_zone.type(x) == "line":
                    width = int(float(self.draw_zone.itemcget(x, 'width')))
                    newwidth = math.ceil((width*1.1)+1)
                    self.draw_zone.itemconfigure(x, width = newwidth)
        #zoom out
        elif (event.delta < 0):
            self.draw_zone.scale("all", truex, truey, 0.9, 0.9)
            self.regZoom *= 0.9
            for x in self.stack:
                if self.draw_zone.type(x) == "text":
                    size = int(self.draw_zone.itemcget(x, 'font')[7:])
                    if size < 2:
                        size = 2
                    newsize = math.ceil((size*0.9)-1)

                    self.draw_zone.itemconfigure(x, font = ("Purisa", newsize))
                if self.draw_zone.type(x) == "line":
                    width = int(float(self.draw_zone.itemcget(x, 'width')))
                    newwidth = math.ceil((width*0.9)-1)
                    if newwidth < 2:
                        newwidth = 2
                    self.draw_zone.itemconfigure(x, width = newwidth)






if __name__ == '__main__':
    ge = Paint()
