"""
This file create a menu window for you to select what deck you want to add card 
in and what lookup function you want to use. It contains an option menu to 
select the deck, a button to refresh the decks, and three buttons to select the 
functions. The required modules are:

- tkinter
- messagebox (tkinter)
- filedialog (tkinter)
- abspath (os.path)
- dirname (os.path)
- chdir (os)
"""
import tkinter as tk
from tkinter import messagebox
import imgrecog
import tkinter.filedialog
import word_lookup
import article_lookup
import add_card
from os.path import abspath, dirname
from os import chdir

class lookupGUI:
    """
    A class to create a menu window. It contains 4 buttons an option menu.

    `refreshButton` is bound with the function `_refreshDecks`. When users 
    click on it, the function will update the connection with anki and refresh 
    the decks listed in the option menu.

    `word_lookup_button`, `article_lookup_button`, `image_lookup_button` are  
    bound with the methods `_wordlookup`, `_articlelookup`, `_imagelookup`, 
    respectively. The mothods use the modules to create new windows.

    `_decksmenu` is an option menu which lists all the decks of the user's anki. 
    The users can select one of it to add new cards in. If the program can not 
    connect with the user's anki, this menu will show nothing.

    Attributes:
        No public attributes.

    """
    def __init__(self):
        self._definitions = ''
        self._master = tk.Tk()
        self._master.title('Anki Auto-Lookup!')
        self._master.geometry('800x600')
        self._master.configure(background='white')
        
        self._deck_name_prompt = tk.Label(self._master, 
                text='Please select the deck you want to add cards to:', 
                bg='white', font=('Arial', 15))
        self._deck_name_prompt.pack()
        
        refreshButton = tk.Button(self._master, text='Refresh', 
                command=self._refreshDecks)
        refreshButton.pack()

        self._targetDeck = tk.StringVar()

        self._decknames = tuple([None])
        self._updateDeckNames()
        self._decksmenu = tk.OptionMenu(self._master, self._targetDeck, 
                *self._decknames)
        self._decksmenu.pack()

        word_lookup_button = tk.Button(self._master, text='Word Lookup', fg='white',
                bg='blue', command=self._wordlookup, font=('Arial', 20), width=20)
        word_lookup_button.pack()

        article_lookup_button = tk.Button(self._master, text='Article Lookup', 
                fg='white', bg='red', command=self._articlelookup, 
                font=('Arial', 20), width=20)
        article_lookup_button.pack()

        image_lookup_button = tk.Button(self._master, text='Image Lookup',
                fg='white', bg='green', command=self._imagelookup,
                font=('Arial', 20), width=20)
        image_lookup_button.pack()
        
        self._master.mainloop() 


    def _imagelookup(self):
        """
        When the user click on `image_lookup_button`, check if the user has 
        selected the deck. If yes, open `ImgRecognitionWindow`. Otherwise, show 
        a message box to remind the user.
        
        Args:
                None

        Return:
                None

        Raise:
                None 
        """
        if add_card._new_deck_name(self._targetDeck.get()) == None:
            messagebox.showerror("Error", "Please select the deck you want to add cards to.")
            return   
        self._master.withdraw() 
        self._imageRecog = imgrecog.ImgRecognitionWindow() 
        self._master.update()
        self._master.deiconify() 


    def _wordlookup(self):
        """
        When the user click on `word_lookup_button`, check if the user has 
        selected the deck. If yes, open `WordLookupWindow`. Otherwise, show 
        a message box to remind the user.
        
        Args:
                None

        Return:
                None

        Raise:
                None
        """  
        if add_card.new_deck_name(self._targetDeck.get()) == None:
            messagebox.showerror("Error", "Please select the deck you want to add cards to.")
            return
        self._master.withdraw() 
        self._wordlookup = word_lookup.WordLookupWindow()
        self._master.update()
        self._master.deiconify() 


    def _articlelookup(self):
        """
        When the user click on `article_lookup_button`, check if the user has 
        selected the deck. If yes, open `ArticleRecognitionWindow`. Otherwise, 
        show a message box to remind the user.
        
        Args:
                None

        Return:
                None

        Raise:
                None 
        """
        if add_card.new_deck_name(self._targetDeck.get()) == None:
            messagebox.showerror("Error", "Please select the deck you want to add cards to.")
            return  
        self._master.withdraw() 
        self._articlelookup = article_lookup.ArticleRecognitionWindow() 
        self._master.update()
        self._master.deiconify() 

    def _getDecks(self):
        """
        Called by the method `_updateDeckNames`. This method use the API to get 
        the deck names in the user's anki.
        
        Args:
                None

        Return:
               A list contains all the deck names in the user's anki. 

        Raise:
                None 
        """
        r = add_card.Request('deckNames')
        return r._response['result']

    def _updateDeckNames(self):
        """
        Called by the method `_refreshDecks`. this method changes the list got 
        from `_getDecks` into tuple and put them in the attribute `_decknames`. 
        If the program can not connect with the user's anki, it will show a 
        warning caption.
        
        Args:
                None

        Return:
                None

        Raise:
                Raise Exception('Failed to connect with API. Please check that 
                you have all the prerequisite installed then click"refresh".') 
                if the program can not connect with the anki API.
        """
        try:
            dn = self._getDecks()
            self._decknames = tuple(dn)
            self._deck_name_prompt.configure(text='Please select the deck you want to add cards to: ')
 
        except Exception as e:
            self._decknames = tuple([None])
            self._deck_name_prompt.configure(text='Failed to connect with API. Please check that you have\nall the prerequisite installed then click "refresh".')
            # raise e
 
    def _refreshDecks(self):
        """
        When the user click on `refreshButton`, reconnect to the user's anki 
        and update the names of the deck in it. Also, refresh the options in the 
        option menu.
        
        Args:
                None

        Return:
                None

        Raise:
                None 
        """
        self._targetDeck.set('')
        self._updateDeckNames()
        self._deck_name_prompt.update()
        self._decksmenu['menu'].delete(0, 'end') 
        for option in self._decknames:
            self._decksmenu['menu'].add_command(label=option, 
                    command=tk._setit(self._targetDeck, option)) 




if __name__ == '__main__':
    chdir(dirname(abspath(__file__)))
    dao = lookupGUI()

