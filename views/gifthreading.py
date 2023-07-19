import os
import threading
import tkinter as tk

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.background = self['bg']
        self.bind("<Enter>", self.hover)
        self.bind("<Leave>", self.leave)

    def hover(self, e):
        self['bg'] = self['activebackground']
    def leave(self, e):
        self['bg'] = self.background

class GifThread(threading.Thread):
    def __init__(self, window, label, frameCnt, file_name, x, y, color):
        threading.Thread.__init__(self)
        self.window = window
        self.label = label
        self.frameCnt = frameCnt
        self.file_path = os.path.join(os.path.dirname(__file__), file_name)
        self.x = x
        self.y = y
        self.color = color

    def run(self):
        frames = [tk.PhotoImage(file=self.file_path, format=f"gif -index {i}") for i in range(self.frameCnt)]
        for i in range(self.frameCnt):
            frames[i] = frames[i].subsample(3, 3)
        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == self.frameCnt:
                ind = 0
            try:
                self.label1.configure(image=frame)
            except:
                pass
            self.window.after(100, update, ind)
        self.label1 = tk.Label(self.label, background=self.color)
        self.label1.place(x=self.x, y=self.y)
        self.window.after(0, update, 0)
        return self.label1

class GifContent(threading.Thread):
    def __init__(self, window, label, frameCnt, file_name, x, y, color):
        threading.Thread.__init__(self)
        self.window = window
        self.label = label
        self.frameCnt = frameCnt
        self.file_path = os.path.join(os.path.dirname(__file__), file_name)
        self.x = x
        self.y = y
        self.color = color

    def run(self):
        frames1 = [tk.PhotoImage(file=self.file_path, format=f"gif -index {i}") for i in range(self.frameCnt)]
        for i in range(self.frameCnt):
            frames1[i] = frames1[i].subsample(2, 2)
        def update(ind):
            frame = frames1[ind]
            ind += 1
            if ind == self.frameCnt:
                ind = 0
            try:
                self.label2.configure(image=frame)
            except:
                pass
            self.window.after(100, update, ind)
        # change the name every time you use this function
        self.label2 = tk.Label(self.label, background=self.color)
        self.label2.place(x=self.x, y=self.y)
        self.window.after(0, update, 0)