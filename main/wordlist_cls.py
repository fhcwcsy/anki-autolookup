import tkinter as tk
import crawler
import time
import threading
import add_card

INTERVAL = 1
 

class WordlistWindow(tk.Frame):
    """A class defining the window listing all the words to be added.
    
    The design of this class is based on the answer here:
    https://stackoverflow.com/questions/23483629/dynamically-adding-checkboxes-into-scrollable-frame

    This class inherit tk.Frame. Initiate the window by  constructing an
    instance as a normal tk.Frame:

        w = WordlistWindow(master)

    Then pack to show the frame. Note that if you use more than one Tk objects at
    a time, then this master Tk object must be constructed first or there will
    be errors, reasons unknown. Use
    
        w.newWord('MyWord')

    to add new word. The word should pop up in the list immediately, unless it
    is already in the list. A lookup process will be initiated in the background
    once the object is constructed. Each word added with newWord() method will
    be added to a queue, and will be looked up one by one in the background with
    threading module. The words added to the list should have its checkbutton 
    checked by default (if not, then something's wrong! Please make sure that
    this window is the first Tk object constructed in the script.) The user can 
    click on the "done" button to quit. The program will wait until the queue is
    empty, then add all the checked words to anki, then quit.

    Attributes:
        vscrollbar: The vertical tk.Scrollbar object on the right.
        canvas: The tk.Canvas in the background of the frame.
        interior: a tk.Frame object that everything lie on.
    """
    def __init__(self, master, quitFunc, **kwargs):
        """Construct a modified tk.Frame object with scrollbar and word checklist.

        Constructor. Inherit the Frame class from tk, while adding a scrollbar,
        and word listing feature. Takes all arguments as tk.Frame

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
        self.quitButton = tk.Button(self.interior, text='Done', command=self.quitAndAdd)
        self.quitButton.grid(row=1, column=1)

        # Wordlist setup
        self._cbvar = []
        self._cb = []
        self._queue = []
        self._finished = []
        self._finishedWord = []
        self._thread = True
        self._interval = INTERVAL
        self._threadInstance = threading.Thread(target=self._lookupTreading, args=())
        self._threadInstance.daemon = True
        self._threadInstance.start()

        self._quitFunction = quitFunc

        self.updateTimer()

    def _lookupTreading(self):
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



    def updateTimer(self):
        self._status.config(text=f'Status: queue {len(self._queue)}/{len(self._queue)+len(self._finishedWord)}')
        self._status.after(500, self.updateTimer)


    def quitAndAdd(self):
        """Add the words checked and quit.

        Called when the user hit the "quit" button. The function wait until all
        cards have been looked up (the queue is empty), then add all cards to
        deck, and finally quit the window. 
..
        Args:
            None
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
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def newWord(self, word):
        """Add new words

        function to add new word. load the word in to the queue, then the method
        _lookupTreading will look them up in the background.

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


 
