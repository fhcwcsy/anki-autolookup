import tkinter as tk
import tkinter.filedialog
import imgrecog

class ImgRecognitionWindow:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, n=None):
        self._img_path = tk.filedialog.askopenfilename(title=
                'Choose your image.')

        tp = imgrecog.TextPicture(self._img_path)
         
        master = tk.Tk()
        master.title('Text Recognition')
        tkimg = imgrecog.ImageTk.PhotoImage(tp.originalImg) 
        master.geometry('{}x{}'.format(*tp.processedImg.size))
        master.resizable(width=False, height=False)
        pic = tk.Label(master, image = tkimg)
        pic.pack(side = "bottom", fill = "both", expand = "yes") 
        pic.bind('<Button-1>', tp.bindEvent)
        tk.mainloop()
         

if __name__ == "__main__":
    w = ImgRecognitionWindow()


