# -*- coding: utf-8 -*-
"""
This file will create a window .Users can select a picture file, and it 
would be shown in this window.When users click on the word of it, this program 
will recognize the word and generate the vocabulary card.The required modules
are:
-  PIL
-  numpy
-  pytesseract
-  re
-  tkinter
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
from tkinter import messagebox
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
    """
    When the black pixels in a raw is less than this constant,
    we will detect it as a white line.
    """
    _BNW_THRESHOLD = 140
    """
    The constant which will be used to process the picture(see imgArray below).
    When the number is larger than it, we will detect it as white and set it
    to be 0. Otherwise, we will detect is as black and set it to be 1.
    """
    SPACE_THRESHOLD = 2
    """
    When the black pixels in a column is less than it,
    we detect it as a white column.
    """
    def __init__(self, img):
        """Constructor. Takes the path to the picture as an argument. """
        self.originalImg = img #The target picture to be recognized.
        self.imgArray = np.floor_divide(
                np.array(self.originalImg.convert('L')), TextPicture._BNW_THRESHOLD)
        self.processedImg = Image.fromarray(np.multiply(self.imgArray, 255))
        """
        The processed image mentioned in imgArray.
        """
        self.height, self.width = self.imgArray.shape #The size of the picture.
        
        self.imgArray = np.subtract(1, self.imgArray)
        """The array of the image, which is processed a little bit to make it
        more easliy to analyze. (Turn the array to be 0 and 1 only. 0 means
        white, while 1 means black)
        """
        self._horizontalSum = np.sum(self.imgArray, axis=1) 
        """The number of black points of each horiaontal raw of the picture."""
        # plt.matshow(self.processedImg)
        # plt.plot(self._horizontalSum)
        # plt.show() 
         

    def bindEvent(self, event):
        """
        When the event is occured, we will return the word on the 
        position (event.x, event.y)
    
        Args:
                event: The event that triggers the function recognizeWord.
            
        Return:
                recognizeWord(event.x, event.y)
    
        Raise:
                None
        """
        # print(f'mouse location: ({event.x}, {event.y})')
        return self.recognizeWord(event.x, event.y)

    def _is_similar(self, s1,s2):
        """
        Determine whether s1 and s2 are similar or not.

        We would compare the length and the characters in them to determine 
        whether they are similar or not.

        Args:
                s1, s2: two strings to be compared.
        
        Return:
                True: if they are similar.
                False: if they are not.

        Raises:
	        None
        """
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
        """
        This function is designed to recognize the word on the
        position(wordX, wordY).

        Args:
                WordX, WordY: The position of the word we want to recognize.
    
        Return:
                The word we recognize. Type: str
    
        Raise:
                None
        """

        """
        Here, we will first find the nearst white raws to detect the line
        which the word belong to. Use 
        _extractLine(lineUpperBound, lineLowerBound) to divide the words.
        """
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
        """
        Then, we put the image of the line into pytesseract to transform
        image to English. Use the order of the word in the string to
        get targetWordFromLine. But sometimes the order may be detected wrong.
        So we chop the image of the word and use pytesseract to get 
        targetWordFromWord, which may have lower precision than the word
        detected in whole line. 
        """
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
        """
        Last, we use _is_similar(s1, s2) to compare targetWordFromLine and 
        targetWordFromWord. If they are similar, then return 
        targetWordFromLine, which has higher precision. When they are not 
        similar, it implies that the order of the word in line may be
        detected wrong. Thus, targetWordFromLine may be wrong,
        so we return targetWordFromWord instead.
        """
        if self._is_similar(targetWordFromLine, targetWordFromWord):
            return targetWordFromLine
        elif len(targetWordFromWord)==0:
            return targetWordFromLine
        else:
            return targetWordFromWord
         


    def _extractLine(self, lineUpperBound, lineLowerBound):
        """
        This method will analyze the interest region which is given by
        lineUpperBound and lineLowerBound. And this interest region is actually
        a subset of the imgarray.

        We will first sum up vertically to detect the white column. If the
        number of black pixels in a column is less than SPACE_THRESHOLD, we
        recognize it as a white column. Find the wider white column to be the
        divide of two words. And then we return a list of index of divide of words. 

        Args:
                lineUpperBound: The upper bound of raw of the interest region.
                lineLowerBound: The lower bound of raw of the interest region.
        
        Return:
                wordIndices: a list of index of divide of words.

        Raise:
                Exception: raise e
        """
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
    right. More, it is inherited from `TextPicture`
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Here will create two windows.
    
        _picwindow will show the picture users choose (We will let users 
        choose the file they want first). And users can click the word on it.
    
        _wordWindow will show the word users click. And then let the users
        choose which words they want to make the vocabulary cards.

        Args:
                None
    
        Return:
                None
            
        Raise:
                None
        """
        while True:
            try:
                self._img_path = tk.filedialog.askopenfilename(title='Choose your image.')
                img = Image.open(self._img_path)
                break
            except:
                messagebox.showerror('Error', 'File need to be picture.')
                pass

        self._picWindow = tk.Toplevel()
        self._wordWindow = tk.Toplevel()

        resizeRatio = max(img.size[0]/self._wordWindow.winfo_screenwidth()/0.8, 
                img.size[1]/self._wordWindow.winfo_screenheight(), 1)

        # print(resizeRatio)

        if resizeRatio > 1:
            img = img.resize(
                    (int(img.size[0]/resizeRatio),
                    int(img.size[1]/resizeRatio)))
        
        TextPicture.__init__(self, img)
        # exit()

        # picture window settings
        self._picWindow.title('Text Recognition')
        tkimg = ImageTk.PhotoImage(self.originalImg, master=self._picWindow) 
        self._picWindow.geometry('{}x{}+0+0'.format(*self.processedImg.size))
        self._picWindow.resizable(width=False, height=False)
        pic = tk.Label(self._picWindow, image = tkimg)
        pic.pack(side = "bottom", fill = "both", expand = "yes") 
        pic.bind('<Button-1>', self.bindEvent)

        # word window settings
        wwwidth = min(self._wordWindow.winfo_screenwidth()-self.processedImg.size[0], 300)
        self._wordWindow.geometry(f'{wwwidth}x{self.processedImg.size[1]}+{self.processedImg.size[0]}+0')
        self._wordWindow.title('Words to be added')
        self.wlist = wordlist_cls.WordlistWindow(self._wordWindow, self.quitWindow, bg='#444444')
        self.wlist.pack(expand="true", fill="both")

        # self._wordWindow.lift()
        # self._picWindow.lift()
        tk.mainloop()

    def quitWindow(self):
        """
        Destroy / Quit the windows after users used it.

        Args:
                None
            
        Return:
                None
            
        Raise:
                None
        """
        self._wordWindow.destroy()
        self._wordWindow.update()
        self._picWindow.destroy()
        self._picWindow.update()
        self._wordWindow.quit()
        self._picWindow.quit()

    def bindEvent(self, event):
        """
        When the event occured, We will detect the word users click and add it
        to the `_wordWindow`

        Args:
                None
            
        Return:
                None
            
        Raise:
                None
        """
        word = super().bindEvent(event)
        self.wlist.newWord(word)
 

if __name__ == "__main__":
    i = ImgRecognitionWindow()
