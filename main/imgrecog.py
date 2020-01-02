# -*- coding: utf-8 -*-
"""Picture to word analysis

TODO: description

Required modules:
    pytesseract

Example:
    TODO


"""  


from PIL import Image, ImageTk
import numpy as np
import pytesseract
import re
import tkinter.filedialog
# import matplotlib.pyplot as plt
import time
# import math
# from scipy.fftpack import fft,ifft
import tkinter as tk
import wordlist_cls
# import os

def timer(func):
    """
    A simple timer as an decorator
    """
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        print('cost : ',t2-t1)
        return result
    return wrapper 
 

class TextPicture():

    """A picture containing text to be recognized."""

    IMAGE_PATH = './img3.jpg'
    LINE_THRESHOLD = 3
    _BNW_THRESHOLD = 140
    SPACE_THRESHOLD = 2

    def __init__(self, imgPath):
        """Constructor. Takes the path to the picture as an argument. """
        self.originalImg = Image.open(imgPath)
        self.imgArray = np.floor_divide(
                np.array(self.originalImg.convert('L')), TextPicture._BNW_THRESHOLD)
        self.processedImg = Image.fromarray(np.multiply(self.imgArray, 255))
        self.height, self.width = self.imgArray.shape
        self.imgArray = np.subtract(1, self.imgArray)
        self._horizontalSum = np.sum(self.imgArray, axis=1)
        # plt.matshow(self.processedImg)
        # plt.plot(self._horizontalSum)
        # plt.show() 
         

    def bindEvent(self, event):
        # print(f'mouse location: ({event.x}, {event.y})')
        return self.recognizeWord(event.x, event.y)

    def _is_similar(self, s1,s2):
        if abs(len(s1)-len(s2))>2:
            return False
        n = 0
        for each in s1:
            if each in s2:
                pass
            else:
                n+=1
        if n>=int(len(s1)/3)+1:
            return False
        else:
            return True
     

    def recognizeWord(self, wordX, wordY):
        # print('X:', wordX)
        lineUpperBound = wordY
        lineLowerBound = wordY+1
        while self._horizontalSum[lineUpperBound] > 4:
            lineUpperBound -= 1
        while self._horizontalSum[lineLowerBound] > 4:
            lineLowerBound += 1

        # print('bounds:', lineUpperBound, lineLowerBound)
        wordIndices = self._extractLine(lineUpperBound, lineLowerBound)
        for i in range(len(wordIndices)-1):
            if wordIndices[i] <= wordX <= wordIndices[i+1]:
                leftBound = wordIndices[i]
                rightBound = wordIndices[i+1]
                wordOrder = i
                break

        lineCrop = self.originalImg.crop((
                0, lineUpperBound, self.width-1, lineLowerBound))
        lineText = pytesseract.image_to_string(lineCrop, lang = 'eng')
        wordsInLine = re.findall('\w+', lineText)
        # print(wordOrder)
        # print(wordsInLine)
        targetWordFromLine = wordsInLine[wordOrder]
        wordCrop = self.originalImg.crop((
                leftBound, lineUpperBound, rightBound, lineLowerBound))
        targetWordFromWord = pytesseract.image_to_string(wordCrop, lang = 'eng')
        # print(targetWordFromLine, targetWordFromWord)
        # print(targetWordFromLine)
        if self._is_similar(targetWordFromLine, targetWordFromWord):
            return targetWordFromLine
        elif len(targetWordFromWord)==0:
            return targetWordFromLine
        else:
            return targetWordFromWord
         


    def _extractLine(self, lineUpperBound, lineLowerBound):
        # print(lineUpperBound, lineLowerBound)
        try:
            # sum vertically, convert to bool then back to int so the columns 
            # with no black pixels will be 0 and 1 otherwise
            verticalSum = np.floor_divide(
                    np.sum(self.imgArray[lineUpperBound:lineLowerBound][:],
                    axis=0), TextPicture.SPACE_THRESHOLD).astype(bool).astype(int).astype(str)
            
            # plt.plot(verticalSum)
            # plt.show() 

            lineStr = ''.join(list(verticalSum))
            # print(lineStr)
            whiteSpacesIter = re.finditer('10+1', lineStr)
            # print(list(whiteSpacesIter))
            blackColumns = list(re.finditer('01+0', lineStr))
            whiteSpaceIndices = [(ws.start(), ws.end()) for ws in whiteSpacesIter]
            whiteSpaceSize = [ws[1]-ws[0] for ws in whiteSpaceIndices]
            maxWhiteSpaceSize = max(whiteSpaceSize)
            minWhiteSpaceSize = min(whiteSpaceSize)

            wordIndices = [blackColumns[0].start()]
            for i in range(len(whiteSpaceIndices)):
                if (maxWhiteSpaceSize - whiteSpaceSize[i]) <= (
                        whiteSpaceSize[i] - minWhiteSpaceSize):
                    wordIndices.append(
                            (whiteSpaceIndices[i][0] + whiteSpaceIndices[i][1])//2)
                    # print(whiteSpaceSize[i])
            wordIndices.append(blackColumns[-1].end())
            # print(wordIndices)
            return wordIndices

        except Exception as e:
            # return []
            raise e

class ImgRecognitionWindow(TextPicture):
    """
    A singleton class. Defines the window showing the image. The user clicks
    on words they want to look up and it will be shown in the wordlist on the
    right.
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.wordWindow = tk.Tk()
        picWindow = tk.Tk()
        self._img_path = tk.filedialog.askopenfilename(title=
                'Choose your image.')
        TextPicture.__init__(self, self._img_path)

        # picture window settings
        picWindow.title('Text Recognition')
        tkimg = ImageTk.PhotoImage(self.originalImg, master=picWindow) 
        picWindow.geometry('{}x{}+0+0'.format(*self.processedImg.size))
        picWindow.resizable(width=False, height=False)
        pic = tk.Label(picWindow, image = tkimg)
        pic.pack(side = "bottom", fill = "both", expand = "yes") 
        pic.bind('<Button-1>', self.bindEvent)

        # word window settings
        wwwidth = min(self.wordWindow.winfo_screenwidth()-self.processedImg.size[0], 150)
        self.wordWindow.geometry(f'{wwwidth}x{self.wordWindow.winfo_screenheight()}+{self.processedImg.size[0]}+0')
        self.wordWindow.title('Words to be added')
        self.wlist = wordlist_cls.WordlistWindow(self.wordWindow, bg='#444444')
        self.wlist.pack(expand="true", fill="both")

        tk.mainloop()

    def bindEvent(self, event):
        word = super().bindEvent(event)
        self.wlist.newWord(word)
 

if __name__ == "__main__":
    i = ImgRecognitionWindow()
