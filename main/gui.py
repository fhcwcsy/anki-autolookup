import tkinter as tk
import imgrecog
import tkinter.filedialog
import word_lookup
import article_lookup

class lookupGUI:
    def __init__(self):

        self.definitions = ''

        window = tk.Tk()
        window.title('Anki Auto-Lookup!')
        window.geometry('400x300')
        window.configure(background='white')
        
        word_lookup_button = tk.Button(window, text='Word Lookup', fg='white', bg='blue', command=self.word_lookup, font=('Arial', 20), width=20)
        word_lookup_button.pack()

        article_lookup_button = tk.Button(window, text='Article Lookup', fg='white', bg='red', command=self.article_lookup, font=('Arial', 20), width=20)
        article_lookup_button.pack()

        image_lookup_button = tk.Button(window, text='Image Lookup', fg='white', bg='green', command=self.image_lookup, font=('Arial', 20), width=20)
        image_lookup_button.pack()



        window.mainloop() 
 

    def image_lookup(self):
        imgrecog.ImgRecognitionWindow() 


    def word_lookup(self):
        word_lookup.word_lookupWindow()
    def article_lookup(self):
        article_lookup.ArticleRecognitionWindow()
 


def article_lookup():
    # TODO
    pass

def image_lookup():
    # TODO
    pass


'''
def jump():
    jump = tk.Toplevel()
    jump.title('hi!')
'''


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
    dao = lookupGUI()

