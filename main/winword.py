import tkinter as tk
import crawler
import time
import datetime
import threading

INTERVAL = 2
 

class WordlistWindow(tk.Frame):
    def __init__(self, master, **kwargs):
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

        self.bind('<Configure>', self.set_scrollregion)

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

    def _lookupTreading(self):
        while self._thread:
            # print('thread running')
            while len(self._queue) == 0:
                # print('current list', len(self._finishedWord))
                time.sleep(self._interval)
            print('unfinished:', len(self._queue))
            word = self._queue[0]
            request = crawler.LookupRequest(word) 
            request.onlineLookup()
            entries = request.export()
            # TODO: what if the lookup failed?
            self._finished.append(entries)
            self._finishedWord.append(word)
            self._queue.remove(word)

    def quitAndAdd(self):
        # print(list(zip(self._finishedWord, self._cbvar))) # TODO: replaced with adding cards
        for b in self._cbvar:
            print(b.get())
        self.winfo_toplevel().quit()


    def set_scrollregion(self, event=None):
        """ Set the scroll region on the canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def newWord(self, word):
        if not ((word in self._finishedWord) and (word in self._queue)):
            self._cbvar.append(tk.BooleanVar())
            self._cbvar[-1].set(True)
            self._cb.append(tk.Checkbutton(self.interior, text=word,
                var=self._cbvar[-1]))
            self._cb[-1].grid(row=(len(self._cb) + 2), column=1, sticky='w')
            self._queue.append(word)
            self.set_scrollregion()
# def add_button():
    # tk.Button(checkbox_pane.interior, text='New Button', command=add_button).pack()
    # checkbox_pane.set_scrollregion()

if __name__ == "__main__":
    root = tk.Tk()
    ww = WordlistWindow(root, bg='#444444')
    ww.pack(expand="true", fill="both")
    ww.newWord('weeeee')
    ww.newWord('weeeee2')

    root.mainloop() 

# main_button = tk.Button(ww.interior,text='Press to add button',command=add_button).pack()

 
