"""
    anki-autolookup.wordlist_cls
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This file defines the WordlistWindow class, which is the window with all the
    word added to be looked up. It uses threading module to lookup in the
    background.
"""

import tkinter as tk
import crawler
import time
import threading
import add_card

INTERVAL = 1
 

class WordlistWindow(tk.Frame):
    """A class defining the frame listing all the words to be added.
    
    The design of this class is based on the answer here:
    https://stackoverflow.com/questions/23483629/dynamically-adding-checkboxes-into-scrollable-frame

    This class inherit tk.Frame. Initiate the window by  constructing an
    instance as a normal tk.Frame:

        w = WordlistWindow(master, quitFunc)

    Then pack/grid to show the frame. Use
    
        w.newWord('MyWord')

    to add a new word. The word should pop up in the list immediately, unless it
    is already in the list. A lookup process will be initiated in the background
    once the object is constructed. Each word added with newWord() method will
    be added to a queue, and will be looked up one by one in the background with
    threading module. The words added to the list should have its checkbutton 
    checked by default. The user can click on the "done" button to quit and 
    quitFunc() will be called, which can be used to close the window.

    Attributes:
        vscrollbar: The vertical tk.Scrollbar object on the right.

        canvas: The tk.Canvas in the background of the frame.
        
        interior: a tk.Frame object that everything lie on.

        vscrollbar: The vertical tk.Scrollbar object on the right.

        canvas: The `tk.Canvas` in the background of the frame.

        interior: `a tk.Frame` object that everything lie on.

        _status: a `tk.Label` object showing the length of the queue.

        _quitButton: a `tk.Button` object that will quit the window while
            pressed.

        _cbvar: A list of `tk.BooleanVar` objects saving and monitoring the
            value of the checkbutton of each word.

        _cb: A list of `tk.Checkbutton` objects, one for each word, and linked
            to the corresponding `tk.BooleanVar` objects in `self._cbvar`.

        _queue: A list of strings saving the words that are added via
            `self.newWord(word)` and are not yet looked up.

        _finished: A list of list of Entry objects saving the lookup result of
        each word. `None` if the lookup failed.

        _finishedWord: A list of strings saving the words that have been
            looked up.

        _thread: A boolean. If set to `False`, the lookup threading will
            pause.

        _interval: The length of time to wait while the queue is empty.

        _threadInstance: A `threading.Thread` object controlling the
            lookup in the background.

        _quitFunction: A function. Will be called when `self._quitButton`
            is pressed to kill the window.
 
    """

    def __init__(self, master, quitFunc, **kwargs):
        """Construct a modified tk.Frame object with scrollbar and word checklist.

        Constructor. Inherit the Frame class from tk, while adding a scrollbar,
        and word listing feature. Takes all arguments as tk.Frame.

        Args:
            same as tk.Frame.

        Return:
            None

        Raises:
            None
        """
        # Scrollable frame setup
        tk.Frame.__init__(self, master, **kwargs)

        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(side='right', fill="y",  expand="false")
        self.canvas = tk.Canvas(self,
                                bg='#444444', bd=0,
                                height=350,
                                highlightthickness=0,
                                yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand="true")
        self.vscrollbar.config(command=self.canvas.yview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = tk.Frame(self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self.interior, anchor="nw")

        self.bind('<Configure>', self._set_scrollregion)

        # status text
        self._status = tk.Label(self.interior, text='Status: idle')
        self._status.grid(row=2, column=1)

        # done button
        self._quitButton = tk.Button(self.interior, text='Done', command=self._quitAndAdd)
        self._quitButton.grid(row=1, column=1)

        # Wordlist setup
        self._cbvar = []
        self._cb = []
        self._queue = []
        self._finished = []
        self._finishedWord = []
        self._thread = True
        self._interval = INTERVAL
        self._threadInstance = threading.Thread(target=self._lookupThreading, args=())
        self._threadInstance.daemon = True
        self._threadInstance.start()

        self._quitFunction = quitFunc

        self._updateStatus()

    def _lookupThreading(self):
        """Look up words in self._queue in the background.

        Uses threading module to implement multitasking, so it will continue to
        lookup words (the speed depends on the internet speed) while the user
        input words (the speed depends on CPU and GPU).

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        while self._thread:
            # print('thread running')
            # self._status.config(text=f'Status: progress {len(self._queue)}/{len(self._queue) + len(self._finishedWord)}')
            while len(self._queue) == 0:
                # print('current list', len(self._finishedWord))
                # print('im keep running...')
                time.sleep(self._interval)
            # print('unfinished:', len(self._queue))
            word = self._queue[0]
            request = crawler.LookupRequest(word) 
            request.onlineLookup()
            entries = request.export()
            self._finished.append(entries)
            self._finishedWord.append(word)
            self._queue.remove(word)



    def _updateStatus(self):
        """
        Update the status label to indicate the queue length.
        """

        self._status.config(text=f'Status: queue {len(self._queue)}/{len(self._queue)+len(self._finishedWord)}')
        self._status.after(500, self._updateStatus)


    def _quitAndAdd(self):
        """Add the words checked and quit.

        Called when the user hit the "quit" button. The function wait until all
        cards have been looked up (the queue is empty), then add all cards to
        deck, and finally quit the window. 

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self._quitFunction()

        while len(self._queue) != 0:
            time.sleep(INTERVAL)

        for i in range(len(self._finishedWord)):
            if self._cbvar[i].get() == True and self._finished[i] != None:
                try:
                    add_card.create_model()
                    add_card.add_note(self._finished[i])
                    print('added:', self._finishedWord[i])
                except Exception as e:
                    print('Can not add this word:', self._finishedWord[i])
                    print(str(e))
        # for b, listOfEntries in zip(self._cbvar, self._finished):
            # print(b.get(), listOfEntries) # If b is true, then add the corresponding entries.
    

    def _set_scrollregion(self, event=None):
        """
        Update scroll region of the scrollbar.
        """

        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def newWord(self, word):
        """Add new words

        function to add new word. load the word in to the queue, then the method
        _lookupThreading will look them up in the background.

        Args:
            word: The word to be added.

        Returns:
            None

        Raises:
            None
        """
        if not ((word in self._finishedWord) or (word in self._queue)):
            self._cbvar.append(tk.BooleanVar())
            self._cbvar[-1].set(True)
            self._cb.append(tk.Checkbutton(self.interior, text=word,
                var=self._cbvar[-1]))
            self._cb[-1].grid(row=(len(self._cb) + 3), column=1, sticky='w')
            self._queue.append(word)
            self._set_scrollregion()

if __name__ == "__main__":
    root = tk.Tk()
    ww = WordlistWindow(root, bg='#444444')
    ww.pack(expand="true", fill="both")
    ww.newWord('weeeee')
    ww.newWord('weeeee2')

    root.mainloop() 


 
