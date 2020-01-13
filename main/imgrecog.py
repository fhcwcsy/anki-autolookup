"""
This file can lookup words from an image. The user select a picture, then it 
will be shown in a window. When the user click on the word in the picture, this
program will attempt to recognize the word and generate the vocabulary card. 
Note that the picture must be very well taken so that the lines are not tilted
or bent too much. Some examples are provided in ./imgexample/ . The required 
modules are:

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

    # When the number of black pixels in a raw is less than this number,
    # it will be recognized as a white line.
    _LINE_THRESHOLD = 3 

    # When the gray scale number of a pixel is smaller than this constant, it will
    # be recognized as a white pixel and set to 0. Otherwise, it will be
    # recognized as a black pixel and set to 1.
    _BNW_THRESHOLD = 140

    # When the black pixels in a column is less than this constant,
    # it will be considered as a white column.
    SPACE_THRESHOLD = 2

    def __init__(self, img):
        """Constructor. Takes the path to the picture as an argument. """
        self._originalImg = img #The target picture to be recognized.
        self._imgArray = np.floor_divide(
                np.array(self._originalImg.convert('L')), TextPicture._BNW_THRESHOLD)
        self._processedImg = Image.fromarray(np.multiply(self._imgArray, 255))
        """
        The processed image mentioned in _imgArray.
        """
        self._height, self._width = self._imgArray.shape #The size of the picture.
        
        self._imgArray = np.subtract(1, self._imgArray)
        """The array of the image, which is processed a little bit to make it
        more easliy to analyze. (Turn the array to be 0 and 1 only. 0 means
        white, while 1 means black)
        """
        self._horizontalSum = np.sum(self._imgArray, axis=1) 
        """The number of black points of each horiaontal raw of the picture."""
        # plt.matshow(self._processedImg)
        # plt.plot(self._horizontalSum)
        # plt.show() 
         

    def _bindEvent(self, event):
        """
        When the event is occured, we will return the word on the 
        position (event.x, event.y)
    
        Args:
            event: The event that triggers the function recognizeWord.
            
        Return:
            The word recognized at position (event.x, event.y)
    
        Raise:
                None
        """

        return self.recognizeWord(event.x, event.y)

    def _is_similar(self, s1, s2):
        """
        Determine whether two words s1 and s2 are similar or not.

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
        lineCrop = self._originalImg.crop((
                0, lineUpperBound, self._width-1, lineLowerBound))
        lineText = pytesseract.image_to_string(lineCrop, lang = 'eng')
        wordsInLine = re.findall('\w+', lineText)
        # print(wordOrder)
        # print(wordsInLine)
        targetWordFromLine = wordsInLine[wordOrder]
        wordCrop = self._originalImg.crop((
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
        This method will analyze the a region which is defined by
        lineUpperBound and lineLowerBound. This region should contain the line
        to be analyzed.

        We will first sum up vertically to detect the white column. If the
        number of black pixels in a column is less than _SPACE_THRESHOLD, we
        recognize it as a white column. Then, we find the wider white column to
        be the space between two words. Everything between two spaces is a word.
        Lastly, we return a list of indices to represent the coordinates of each
        word.

        Args:
            lineUpperBound: The upper bound of raw of the interest region.
            lineLowerBound: The lower bound of raw of the interest region.
        
        Return:
            wordIndices: a list of index of divide of words.

        Raise:
            None
        """
        # print(lineUpperBound, lineLowerBound)
        try:
            # sum vertically, convert to bool then back to int so the columns 
            # with no black pixels will be 0 and 1 otherwise
            verticalSum = np.floor_divide(
                    np.sum(self._imgArray[lineUpperBound:lineLowerBound][:],
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
            return []

class ImgRecognitionWindow(TextPicture):
    """
    Defines the window showing the image. The user clicks
    on words they want to look up and the word will be listed in the wordlist 
    on the right. This class inherit the class `TextPicture`
    """

    def __init__(self):
        """
        This constructor will create two windows.
    
        _picwindow will show the picture the user has chosen (We will let the user 
        choose the file they want to be analyzed). Then, the user can click the
        word and the word will be recognized.
    
        _wordWindow will show the selected words. The user can choose which 
        words they want to make the vocabulary cards.

        Args:
            None
    
        Return:
            None
            
        Raise:
            None

        """
        while True:
            try:
                self._img_path = tk.filedialog.askopenfilename(
                        title='Choose your image.')
                img = Image.open(self._img_path)
                break
            except:
                messagebox.showerror('Error', 'The file needs to be picture.')
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

        # picture window settings
        self._picWindow.title('Text Recognition')
        tkimg = ImageTk.PhotoImage(self._originalImg, master=self._picWindow) 
        self._picWindow.geometry('{}x{}+0+0'.format(*self._processedImg.size))
        self._picWindow.resizable(width=False, height=False)
        pic = tk.Label(self._picWindow, image = tkimg)
        pic.pack(side = "bottom", fill = "both", expand = "yes") 
        pic.bind('<Button-1>', self._bindEvent)

        # word window settings
        ww_width = min(self._wordWindow.winfo_screenwidth() - 
                self._processedImg.size[0], 300)

        self._wordWindow.geometry(
            f'{ww_width}x{self._processedImg.size[1]}+{self._processedImg.size[0]}+0')

        self._wordWindow.title('Words to be added')
        self.wlist = wordlist_cls.WordlistWindow(self._wordWindow,
                self.quitWindow, bg='#444444')

        self.wlist.pack(expand="true", fill="both")

        # self._wordWindow.lift()
        # self._picWindow.lift()
        tk.mainloop()

    def quitWindow(self):
        """
        Destroy/quit the windows.

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

    def _bindEvent(self, event):
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
        word = super()._bindEvent(event)
        self.wlist.newWord(word)
 

if __name__ == "__main__":
    i = ImgRecognitionWindow()
