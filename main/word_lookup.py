import tkinter as tk
import wordlist_cls


'''
class Application(tk.Frame):
    def __init__(self, self._inputWindow=None):
        tk.Frame.__init__(self, self._inputWindow)
        self.createWidgets()
                
        
    def createWidgets(self):
'''      
                

    
    

class WordLookupWindow(object):

    def __init__(self):
        self.count = 1.0
        
        self._wordlistWindow = tk.Toplevel()
        self._inputWindow = tk.Toplevel()
        self._inputWindow.title('Word Lookup!')
        self._inputWindow.geometry('400x500+300+300')

        # self._inputWindow.configure(background='blue') 
        
        word_lookup_frame = tk.Frame(self._inputWindow)
        word_lookup_frame.pack(side=tk.TOP)
        word_lookup_label = tk.Label(self._inputWindow, text='Word to lookup: ',
                bg='white', font=('Arial', 12))
        word_lookup_label.pack(side=tk.TOP) 

        self.outputbox = tk.Text(self._inputWindow, width=60, height=40)
        self.outputbox.pack()
        self.outputbox.bind('<Return>', self._fireOnEnter)
        self.outputbox.bind('<BackSpace>', self._back)

        self._wordlistWindow.geometry('300x500+700+300') 
        self._wordlistWindow.title('Words to be added')
        self._wordlistInner = wordlist_cls.WordlistWindow(
                self._wordlistWindow, self._quitWindow, bg='#444444')
        self._wordlistInner.pack(expand="true", fill="both")  


        tk.mainloop() 

    def _quitWindow(self):
        self._wordlistWindow.destroy()
        self._wordlistWindow.update()
        self._wordlistWindow.quit()

        self._inputWindow.destroy()
        self._inputWindow.update()
        self._inputWindow.quit()


    def _fireOnEnter(self, event):
        word = self.outputbox.get(self.count, self.count+1)
        self.count += 1
        self.word = word[:-1]
        self._wordlistInner.newWord(self.word)

    def _back(self, event):
        self.count -= 1




if __name__ == '__main__':
    dao = WordLookupWindow()
