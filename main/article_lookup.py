import tkinter as tk
from openpyxl import load_workbook
import re
import wordlist_cls


class ArticleRecognitionWindow():
    def __init__(self):
        self._threshold = 0
        self._inputWindow = tk.Toplevel()
        self._wordwindow = tk.Toplevel()
        self._inputWindow.title('Article Lookup')
        self._inputWindow.geometry('800x600+0+0')

        self._inputWindow.configure(background = 'black')
        text_lookup_frame = tk.Frame(self._inputWindow)
        text_lookup_frame.pack(side = tk.TOP)
        text_lookup_label = tk.Label(self._inputWindow, text = 'Article to lookup: ', 
                bg = 'white', font = ('Arial',12))
        text_lookup_label.pack(side = tk.TOP)
        self.outputbox = tk.Text(self._inputWindow)
        self.outputbox.pack()
        self._wordwindow.geometry('300x600+{}+0'.format(

        self._wordwindow.title('Words to be added')
        self.wlist = wordlist_cls.WordlistWindow(self._wordwindow, self._quitWindow, bg = '#444444')
        self.wlist.pack(expand = 'true', fill = 'both')

        self._inputWindow.mainloop()

    def _quitWindow(self):
        self._inputWindow.destroy()
        self._inputWindow.update()
        self._inputWindow.quit()
        self._wordwindow.destroy()
        self._wordwindow.destroy()
        self._wordwindow.quit()
        
    def lookup(self):
        text = self.outputbox.get('1.0','end')
        worddic = self.getWordlist()
        wordset = self.getArticle(text)
        wordlist = self.setLookup(wordset,worddic)
        for word in wordlist:
            self.wlist.newWord(word)

    def getWordlist(self):
        WBPATH = './dic.xlsx'
        ws = load_workbook(WBPATH)['Freq']
        freq_max = ws['B2'].value
        wordlist = {}
        for i in range(2,22233):
            wordlist[ws['A{}'.format(i)].value] = ws['B{}'.format(i)].value / freq_max
        return wordlist
    def getArticle(self,text):
        words = set()
        splitchars = '[\s+,.\'"]'
        words.update(re.split(splitchars, text.lower()))
        return words
    def dictLookup(self,word, d): 
        w = word
        result = d.get(w, 0)
        if result:
            return word, result

        if w[-1] == 's':
            w = w.strip('s')
            result = d.get(w, 0)
            if result:
                return w, result
            w = word

        if w[-2:] == 'es':
            w = w.strip('es')
            result = d.get(w, 0)
            if result:
                return w, result
            w = word

        if w[-2:] == 'ed':
            w = w.strip('ed')
            result = d.get(w, 0)
            if result == 0:
                w = w.strip('d')
                result = d.get(w, 0)
            if result:
                return w, result
            w = word
        return None
    def setLookup(self, s, dictionary):
        """Look up each word in the set in the local wordlist. If the word is found and its frequency is below the self._threshold, then do online lookup. Stopwords are remov    ed.
    Arguments:
    s: a set containing the words to be looked up.
    dictionary: the dictionary with the key be the words and the value be its frequency.
    return: a list containing tuples of (difficult_words, definition)
    """

        stopWords = ['', 'is', 'are', 'were', 'was', 'have', 'has', 's']
        vocabList = []
        for be in stopWords:
            if be in s:
                s.remove(be)
        for word in s:
            lookupResult = self.dictLookup(word, dictionary)
            if lookupResult == None:
                continue
            if 0 < lookupResult[1] < self._threshold:
                vocabList.append(word)
        return vocabList


if __name__=='__main__':
    done = ArticleRecognitionWindow()
