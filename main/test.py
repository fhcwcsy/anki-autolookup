import tkinter as tk
from PIL import ImageTk, Image 
import os

def motion(event):
  print("Mouse position: (%s %s)" % (event.x, event.y))
  return

master = tk.Tk()
master.title('This is a freaking test')
img = Image.open('test.png')
tkimg = ImageTk.PhotoImage(img) 
master.geometry('{}x{}'.format(*img.size))
pic = tk.Label(master, image = tkimg)
pic.pack(side = "bottom", fill = "both", expand = "yes") 
pic.bind('<Button>',motion)
# master.pack()
tk.mainloop()
