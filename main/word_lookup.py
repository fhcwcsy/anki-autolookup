"""
This file creates a lookup window that you can key in the words you want to 
search. Whenever you press "Enter", it will catch the word you just keyed in. 
Then you can choose what words you want to make the vocabulary cards in anki. 
The required module is:

- tkinter
"""

import tkinter as tk
import wordlist_cls

class WordLookupWindow(object):
    """
    Create two windows.

    One is `_inputWindow`, which shows a text box for users to key in words.
    
    The other is `_wordlistWindow`, which shows the words the users just 
    keyed in.

    Attribute:
        _wordlistWindow: A `tk.Toplevel` object. The window showing the
            wordlist.

        _inputWindow: A `tk.Toplevel` object. The window with the textbox
            that allow the user to input words.

        _inputBox: A `tk.Text` object. The textbox that allow the user to 
            input words.

        _wordlistFrame: A `WordlistWindow` object. The frame with the words
            that the user have typed and checkbuttons for each word.
     
    """
    def __init__(self):
        self._wordlistWindow = tk.Toplevel()
        self._inputWindow = tk.Toplevel()
        self._inputWindow.title('Word Lookup!')
        self._inputWindow.geometry('400x500+300+300')

        word_lookup_frame = tk.Frame(self._inputWindow)
        word_lookup_frame.pack(side=tk.TOP)
        word_lookup_label = tk.Label(self._inputWindow, text='Word to lookup: ',
                bg='white', font=('Arial', 12))
        word_lookup_label.pack(side=tk.TOP) 

        self._inputBox = tk.Text(self._inputWindow, width=60, height=40)
        self._inputBox.pack()
        self._inputBox.bind('<Return>', self._fireOnEnter)

        self._wordlistWindow.geometry('300x500+700+300') 
        self._wordlistWindow.title('Words to be added')
        self._wordlistFrame = wordlist_cls.WordlistWindow(
                self._wordlistWindow, self._quitWindow, bg='#444444')
        self._wordlistFrame.pack(expand="true", fill="both")  


        tk.mainloop() 

    def _quitWindow(self):
        """
        Destroy/quit the windows after users click "Done".
        
        Args:
            None

        Return:
            None

        Raise:
            None
        """
        self._wordlistWindow.destroy()
        self._wordlistWindow.update()
        self._wordlistWindow.quit()

        self._inputWindow.destroy()
        self._inputWindow.update()
        self._inputWindow.quit()


    def _fireOnEnter(self, event):
        """
        When the users press "Enter", catch the last word the users just keyed 
        in and put it in the wordlist window.
        
        Args:
            event: The action users did. We bind the "Enter" button to 
            this function, so there is no need to fill this argument.
        
        Return:
            None

        Raise:
            None 
        """
        word = self._inputBox.get(1.0, tk.END)
        self.word = word[:-1]
        self.word = self.word.split('\n')
        self._wordlistFrame.newWord(self.word[-1])
        


if __name__ == '__main__':
    dao = WordLookupWindow()
