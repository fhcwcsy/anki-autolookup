import tkinter as tk
import wordlist_cls


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
        
        self.wordWindow = tk.Tk()
        master = tk.Tk()
        master.title('Word Lookup!')
        master.geometry(f'{3*master.winfo_screenwidth()//4}x{master.winfo_screenheight()}+0+0')
        master.configure(background='blue') 
        
        word_lookup_frame = tk.Frame(master)
        word_lookup_frame.pack(side=tk.TOP)
        word_lookup_label = tk.Label(master, text='Word to lookup: ', bg='white', font=('Arial', 12))
        word_lookup_label.pack(side=tk.TOP) 

        self.outputbox = tk.Text(master)
        self.outputbox.pack()
        self.outputbox.bind('<Return>', self.FireonEnter)
        self.outputbox.bind('<BackSpace>', self.Back)

        #copied from imgrecog.py
        self.wordWindow.geometry(f'{self.wordWindow.winfo_screenwidth()//4}x{self.wordWindow.winfo_screenheight()}+{3*self.wordWindow.winfo_screenwidth()//4}+0') 
        self.wordWindow.title('Words to be added')
        self.wlist = wordlist_cls.WordlistWindow(self.wordWindow, bg='#444444')
        self.wlist.pack(expand="true", fill="both")  

        tk.mainloop() 

    def FireonEnter(self, event):
        word = self.outputbox.get(self.count, self.count+1)
        self.count += 1
        self.word = word[:-1]
        self.wlist.newWord(self.word)

    def Back(self, event):
        self.count -= 1




if __name__ == '__main__':
    dao = WordLookupWindow()
