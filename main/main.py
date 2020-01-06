import tkinter as tk
import imgrecog
import tkinter.filedialog
import word_lookup
import article_lookup
import add_card
from os.path import abspath, dirname
from os import chdir

class lookupGUI:
    def __init__(self):

        self.definitions = ''
        self.master = tk.Tk()
        self.master.title('Anki Auto-Lookup!')
        self.master.geometry('800x600')
        self.master.configure(background='white')
        
        deck_name_label = tk.Label(self.master, text='Please enter the deck name you want to add words in.', bg='white', font=('Arial', 15))
        deck_name_label.pack()
        self._deck_name_text = tk.Text(self.master, height=1, width=20)
        self._deck_name_text.pack()
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
        deckname = self._deck_name_text.get(1.0, 2.0)[:-1]
        add_card.new_deck_name(deckname)
 
        self.master.withdraw() 
        self.imageRecog = imgrecog.ImgRecognitionWindow() 
        self.master.update()
        self.master.deiconify() 


    def wordlookup(self):
        deckname = self._deck_name_text.get(1.0, 2.0)[:-1]
        add_card.new_deck_name(deckname)
 
        self.master.withdraw() 
        self._wordlookup = word_lookup.WordLookupWindow()
        self.master.update()
        self.master.deiconify() 


    def articlelookup(self):
        deckname = self._deck_name_text.get(1.0, 2.0)[:-1]
        add_card.new_deck_name(deckname)
 
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

