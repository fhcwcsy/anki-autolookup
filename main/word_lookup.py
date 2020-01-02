import tkinter as tk
import crawler
import add_card



'''
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.createWidgets()
                
        
    def createWidgets(self):
'''      
                

    
    

class WordLookupWindow:
    def __init__(self):
        self.count = 1.0
 
        master = tk.Tk()
        master.title('Word Lookup!')
        master.geometry('800x600')
        master.configure(background='blue') 
       # app = Application(master)
        word_lookup_frame = tk.Frame(master)
        word_lookup_frame.pack(side=tk.TOP)
        word_lookup_label = tk.Label(master, text='Word to lookup: ', bg='white', font=('Arial', 12))
        word_lookup_label.pack(side=tk.TOP) 

        self.outputbox = tk.Text(master)
        self.outputbox.pack()
        self.outputbox.bind('<Return>', self.FireonEnter)

        master.mainloop() 

    def FireonEnter(self, event):
        word = self.outputbox.get(self.count, self.count+1)
        self.count += 1
        self.word = word[:-1]
        self.search()

    def search(self):
        l = crawler.LookupRequest(self.word)
        l.onlineLookup()
        entries = l.export()
        add_card.create_model()
        add_card.add_note(entries) 

if __name__ == '__main__':
    dao = WordLookupWindow()
