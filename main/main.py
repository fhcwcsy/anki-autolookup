import tkinter as tk
import imgrecog
import tkinter.filedialog
import word_lookup
import article_lookup
from os.path import abspath, dirname
from os import chdir

class lookupGUI:
    def __init__(self):

        self.definitions = ''
        self.master = tk.Tk()
        self.master.title('Anki Auto-Lookup!')
        self.master.geometry('400x300')
        self.master.configure(background='white')
        
        word_lookup_button = tk.Button(self.master, text='Word Lookup', fg='white',
                bg='blue', command=self.wordlookup, font=('Arial', 20), width=20)
        word_lookup_button.pack()

        article_lookup_button = tk.Button(self.master, text='Article Lookup', 
                fg='white', bg='red', command=self.articlelookup, 
                font=('Arial', 20), width=20)

        article_lookup_button.pack()

        image_lookup_button = tk.Button(self.master, text='Image Lookup',
                fg='white', bg='green', command=self.imagelookup,
                font=('Arial', 20), width=20)

        image_lookup_button.pack()

        self.master.mainloop() 

    def imagelookup(self):
        self.master.withdraw() 
        self.imageRecog = imgrecog.ImgRecognitionWindow() 
        self.master.update()
        self.master.deiconify() 


    def wordlookup(self):
        self.master.withdraw() 
        self._wordlookup = word_lookup.WordLookupWindow()
        self.master.update()
        self.master.deiconify() 


    def articlelookup(self):
        self.master.withdraw() 
        self._articlelookup = article_lookup.ArticleRecognitionWindow() 
        self.master.update()
        self.master.deiconify() 
 

'''


article_lookup_frame = tk.Frame(window)
article_lookup_frame.pack()
article_lookup_label = tk.Label(article_lookup_frame, text='Article to lookup: ', bg='white', font=('Arial', 12))
article_lookup_label.pack(side=tk.LEFT)
article_lookup_entry = tk.Entry(article_lookup_frame, font=('Arial', 12), bg='White')
article_lookup_entry.pack(side=tk.LEFT)






search_button = tk.Button(window, text='LOOKUP!', command=word_lookup, fg='red', bg='blue', font=('Arial', 20))
search_button.pack()

jump_button = tk.Button(window, text='jump!', command=jump)
jump_button.pack()
'''




if __name__ == '__main__':
    chdir(dirname(abspath(__file__)))
    dao = lookupGUI()

