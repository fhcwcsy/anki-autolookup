import tkinter as tk
from openpyxl import load_workbook
import re
import wordlist_cls
import argparse
from argparse import RawTextHelpFormatter

class ArticleRecognitionWindow():
    def __init__(self):
        self.wordWindow = tk.Tk()
        master = tk.Tk()
        master.title('Article Lookup')
        master.geometry(f'{3*master.winfo_screenwidth()//4}x{master.winfo_screenheight()}+0+0')
        master.configure(background = 'black')
        text_lookup_frame = tk.Frame(master)
        text_lookup_frame.pack(side = tk.TOP)
        text_lookup_label = tk.Label(master, text = 'Article to lookup: ', bg = 'white', font = ('Arial',12))
        text_lookup_label.pack(side = tk.TOP)
        self.outputbox = tk.Text(master)
        self.outputbox.pack()
        self.outputbox.bind('<Return>',self.PressEnter)
        self.wordWindow.geometry(f'{self.wordWindow.winfo_screenwidth()//4}x{self.wordWindow.winfo_screenheight()}+{3*self.wordWindow.winfo_screenwidth()//4}+0')
        self.wordWindow.title('Words to be added')
        self.wlist = wordlist_cls.WordlistWindow(self.wordWindow,bg = '#444444')
        self.wlist.pack(expand = 'true', fill = 'both')
        master.mainloop()
    def PressEnter(self, event):
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
        """Look up each word in the set in the local wordlist. If the word is found and its frequency is below the THRESHOLD, then do online lookup. Stopwords are remov    ed.
    Arguments:
    s: a set containing the words to be looked up.
    dictionary: the dictionary with the key be the words and the value be its frequency.
    return: a list containing tuples of (difficult_words, definition)
    """
        parser = argparse.ArgumentParser(prog='AutoLookup', usage='$ python main.py [optional arguments]', formatter_class=RawTextHelpFormatter ) 
        parser.add_argument('--path', '-p', default='./text.txt', type=str, dest='path', help='Path to the text file. The default value is ./text.txt')
        parser.add_argument('--threshold', '-t', dest='threshold', type=float, default=4e-5, help='A float between 0 and 1. Only more difficult words will be looked up if a \nlower value is specified. The default value is 4e-5.')

        args = parser.parse_args()
        THRESHOLD = args.threshold
        if THRESHOLD > 1 or THRESHOLD < 0:
            raise(Exception('Invalid threshold specified'))
        stopWords = ['', 'is', 'are', 'were', 'was', 'have', 'has', 's']
        vocabList = []
        for be in stopWords:
            if be in s:
                s.remove(be)
        for word in s:
            lookupResult = self.dictLookup(word, dictionary)
            if lookupResult == None:
                continue
            if 0 < lookupResult[1] < THRESHOLD:
                vocabList.append(word)
        return vocabList


if __name__=='__main__':
    done = ArticleRecognitionWindow()