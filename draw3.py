import tkinter as tk

class Example(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)

        # create a canvas where we can demonstrate the technique
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="top", fill="both", expand=True)

        # text items with the tag "editable" will inherit these bindings
        self.canvas.tag_bind("editable","<Double-Button-1>", self.set_focus)
        self.canvas.tag_bind("editable","<Button-1>", self.set_cursor)
        self.canvas.tag_bind("editable","<Key>", self.do_key)
        self.canvas.tag_bind("editable","<Home>", self.do_home)
        self.canvas.tag_bind("editable","<End>", self.do_end)
        self.canvas.tag_bind("editable","<Left>", self.do_left)
        self.canvas.tag_bind("editable","<Right>", self.do_right)
        self.canvas.tag_bind("editable","<BackSpace>", self.do_backspace)
        self.canvas.tag_bind("editable","<Return>", self.do_return)

        # create some sample text
        self.canvas.create_text(20,20, anchor="nw", fill="blue",
                                text="double-click the black text to edit.\n" + \
                                     "Blue text cannot be edited (for\n" + \
                                     "illustrative purposes.")
        self.canvas.create_text(20, 80, anchor="nw", tags=("editable",),
                                text="This text is editable")
        self.canvas.create_text(20, 100, anchor="nw", tags=("editable",),
                                text="Press <Return> when done editing")

    def do_return(self,event):
        '''Handle the return key by turning off editing'''

        self.canvas.focus("")
        self.canvas.delete("highlight")
        self.canvas.select_clear()

    def do_left(self, event):
        '''Move text cursor one character to the left'''

        item = self.canvas.focus()
        if item:
            new_index = self.canvas.index(item, "insert") - 1
            self.canvas.icursor(item, new_index)
            self.canvas.select_clear()

    def do_right(self, event):
        '''Move text cursor one character to the right'''

        item = self.canvas.focus()
        if item:
            new_index = self.canvas.index(item, "insert") + 1
            self.canvas.icursor(item, new_index)
            self.canvas.select_clear()

    def do_backspace(self, event):
        '''Handle the backspace key'''

        item = self.canvas.focus()
        if item:
            selection = self.canvas.select_item()
            if selection:
                self.canvas.dchars(item, "sel.first", "sel.last")
                self.canvas.select_clear()
            else:
                insert = self.canvas.index(item, "insert")
                if insert > 0:
                    self.canvas.dchars(item, insert-1, insert)
            self.highlight(item)

    def do_home(self, event):
        '''Move text cursor to the start of the text item'''

        item = self.canvas.focus()
        if item:
            self.canvas.icursor(item, 0)
            self.canvas.select_clear()

    def do_end(self, event):
        '''Move text cursor to the end of the text item'''

        item = self.canvas.focus()
        if item:
            self.canvas.icursor(item, "end")
            self.canvas.select_clear()

    def do_key(self, event):
        '''Handle the insertion of characters'''

        item = self.canvas.focus()
        if item and event.char >= " ":
            insert = self.canvas.index(item, "insert")
            selection = self.canvas.select_item()
            if selection:
                self.canvas.dchars(item, "sel.first", "sel.last")
                self.canvas.select_clear()
            self.canvas.insert(item, "insert", event.char)
            self.highlight(item)

    def highlight(self, item):
        '''Highlight the given text item to show that it's editable'''

        items = self.canvas.find_withtag("highlight")
        if len(items) == 0:
            # no highlight box; create it
            id = self.canvas.create_rectangle((0,0,0,0), fill="white",outline="blue",
                                              dash=".", tag="highlight")
            self.canvas.lower(id, item)
        else:
            id = items[0]

        # resize the highlight
        bbox = self.canvas.bbox(item)
        rect_bbox = (bbox[0]-4, bbox[1]-4, bbox[2]+4, bbox[3]+4)
        self.canvas.coords(id, rect_bbox)

    def set_focus(self, event):
        '''Give focus to the text element under the cursor'''

        if self.canvas.type("current") == "text":
            self.canvas.focus_set() 
            self.canvas.focus("current") 
            self.canvas.select_from("current", 0)
            self.canvas.select_to("current", "end")
            self.highlight("current")

    def set_cursor(self, event):
        '''Move the insertion point'''

        item = self.canvas.focus()
        if item:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            self.canvas.icursor(item, "@%d,%d" % (x, y))
            self.canvas.select_clear()


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()