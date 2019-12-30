import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        self.outputbox = tk.Text()
        self.outputbox["width"] = 20
        self.outputbox["height"] = 1
        self.outputbox.grid()
        self.outputbox.bind('<Return>', self.FireonEnter)

    def FireonEnter(self, event):
        print('Enter pressed')

root = tk.Tk()
app = Application(root)
root.mainloop() 
