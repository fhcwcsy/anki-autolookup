import tkinter as tk
import crawler
import add_card

class lookupGUI:
    def __init__(self):

        self.definitions = ''

        window = tk.Tk()
        window.title('Anki Auto-Lookup!')
        window.geometry('400x300')
        window.configure(background='white')
        
        word_lookup_button = tk.Button(window, text='Word Lookup', fg='white', bg='blue', command=self.word_lookup, font=('Arial', 20), width=20)
        word_lookup_button.pack()

        article_lookup_button = tk.Button(window, text='Article Lookup', fg='white', bg='red', command=article_lookup, font=('Arial', 20), width=20)
        article_lookup_button.pack()

        image_lookup_button = tk.Button(window, text='Image Lookup', fg='white', bg='green', command=image_lookup, font=('Arial', 20), width=20)
        image_lookup_button.pack()

        window.mainloop() 
 


    def word_lookup(self):
        def search(self):
            self.word = word_lookup_entry.get()
            word = self.word
            print(word)
            l = crawler.LookupRequest(word)
            l.onlineLookup()
            #add_card.create_model()
            entries = l.export()
            #add_card.add_note(entries)
        
            definitions = ''
            for entry in entries:
                for defi in entry.definitions:
                    definitions += defi + ', '
                try:
                    if definitions[-2:] == ', ':
                        definitions = definitions[:-2]
                except:
                    pass
                definitions += '\n'
            self.definitions = definitions
            print(definitions)
            result.insert('insert', definitions)
        word_lookup = tk.Tk()
        word_lookup.title('Word Lookup!')
        word_lookup.geometry('800x600')
        word_lookup.configure(background='blue')

        word_lookup_frame = tk.Frame(word_lookup)
        word_lookup_frame.pack(side=tk.TOP)
        word_lookup_label = tk.Label(word_lookup_frame, text='Word to lookup: ', bg='white', font=('Arial', 12))
        word_lookup_label.pack(side=tk.LEFT)
        word_lookup_entry = tk.Entry(word_lookup_frame, font=('Arial', 12), bg='White')
        word_lookup_entry.pack(side=tk.LEFT)
        
        result = tk.Text(word_lookup, bg='white',fg='blue', font=('Arial', 12), height=3)
        result.pack() 

        search_button = tk.Button(word_lookup, text='Lookup!', fg='blue', bg='white', command=search(self), font=('Arial', 20), width=20)
        search_button.pack()
        

 


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

