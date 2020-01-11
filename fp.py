from PIL import Image, ImageTk
import numpy as np
import pytesseract
import re
import matplotlib.pyplot as plt
import time
import math
from scipy.fftpack import fft,ifft
import tkinter as tk
import os
# convert the picture to gray picture first, and then convert it into array.
def img_to_array(image):
    image = image.convert('L') # convert it to gray
    array = np.array(image)
    # make darker color to black and lighter color to white
    n = len(array)
    m = len(array[0])
    for i in range(n):
        for j in range(m):
            if array[i][j]<125:
                array[i][j] = 0
            else:
                array[i][j] = 255
    im = array_to_img(array)
    return array
# convert the array to image
def array_to_img(array):
       return Image.fromarray((array))
# This function would detect the words in one line and return a list of word index.
def word_analysis(array,raw_up,raw_down):
    try:
        result = ['0' for i in range(len(array[0]))]
        # set the white column(straight) to be '1', and black column to be '0'
        for j in range(len(array[0])):
            n = 0
            for k in range(raw_up,raw_down):
                if array[k][j]==0:
                    n+=1
            if n<=1:
                result[j]='1'
        list_target = []
        list_distance = []
        s = ''.join(result)
        target = re.finditer('01+0',s) # detect the white line.
        start = list(re.finditer('10+1',s))
        # create lists stored the information of the span and width of white columns.
        for each in target:
            list_target.append((each.start(),each.end()))
            list_distance.append(each.end()-each.start())
        maxn= max(list_distance)
        minn= min(list_distance)
        list_slice = [start[0].start()]
        # if the width of the white column is more closer to its maximum, regard it as word slice
        for i in range(len(list_distance)):
            if (maxn-list_distance[i])<=(list_distance[i]-minn):
                list_slice.append(int((list_target[i][1]+list_target[i][0])/2))
        list_slice.append(start[-1].end())
        return list_slice
    except:
        return []
# only for debug. It would draw the line we detect.
def check(filename):
    imarray = img_to_array(filename)
    line = raw_analysis(imarray)
    for a,b in line:
        for i in range(len(imarray[0])):
            imarray[a][i] = 170
            imarray[b-1][i] = 170
    return array_to_img(imarray)
# use Fourirer transform to detect the line. It isn't completed yet.
def raw_analysis(array):
    l = [0 for i in range(len(array))]
    ref = ['0' for i in range(len(l))]
    i = 0
    for sublist in array:
        n = 0
        r = '0'
        for each in sublist:
            if each==0:
                n +=1
                r = '1'
        l[i] = n
        ref[i] = r
        i+=1
    print(l)
    s = ''.join(ref)
    target = re.finditer('0+',s)
    list_len = []
    list_index = []
    for each in target:
        list_len.append(each.end()-each.start())
        list_index.append(each.span())
    threshold = (max(list_len)-min(list_len))/5+min(list_len)
    start = 0
    list_chapter = []
    list_ch_index = []
    for i in range(len(list_len)):
        if list_len[i]>threshold:
            list_chapter.append(l[start:list_index[i][0]])
            list_ch_index.append((start,list_index[i][0]))
            list_chapter.append(l[list_index[i][0]:list_index[i][1]])
            list_ch_index.append((list_index[i][0],list_index[i][1]))
            start = list_index[i][1]
    del list_ch_index[0]
    del list_chapter[0]
    print(list_chapter)
    print(list_ch_index)
    list_frequent = []
    for sublist in list_chapter:
        if not len(sublist)==0:
            y = abs(fft(sublist))
            yf2 = y[range(int(len(y)/2))]
            ll = list(yf2)
            ll[0] = 0
            list_frequent.append(ll.index(max(ll)))
    print(list_frequent)
    list_line = []
    list_line_index = []
    for i in range(len(list_chapter)):
        initial = list_ch_index[i][0]
        if (0 in list_chapter[i]) and (1 in list_chapter[i]) and not list_frequent[i]==0:
            list_conduct = ref[list_ch_index[i][0]:list_ch_index[i][1]]
            s_conduct = ''.join(list_conduct)
            s_target = re.finditer('1+',s_conduct)
            for each in s_target:
                if each.end()-each.start()>1.5*list_frequent[i]:
                    split = round((each.end()-each.start())/list_frequent[i])
                    space =(each.end()-each.start())//split
                    for j in range(split):
                        list_line_index.append((initial+each.start()+space*j,initial+each.start()+space*(j+1)))
                else:
                    list_line_index.append((initial+each.start(),initial+each.end()))
        else:
            list_line.append(list_chapter)
            list_line_index.append(list_ch_index[i])
    return list_line_index
# use for debug only, it will draw the column we detect
def check_column(array,raw_up,raw_down,l):
    for i in range(len(array[0])):
        array[raw_up][i]=170
        array[raw_down][i] = 170
    for i in range(raw_up,raw_down):
        for each in l:
            array[i][each]=170
    im = array_to_img(array)
    im.show()
# to verify if the two words are similar
def is_similar(s1,s2):
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
# put the file and position into it, and it would return the translation of the word which you click.
def pointing_word(img1,imarray,*args):
    raw = args[0]
    column = args[1]
    raw_up = raw
    raw_down = raw+1
    while True:
        n = 0
        for each in imarray[raw_up]:
            if each==0:
                n+=1
        if n<=3: # the threshold of black dots. if the number of black dots is less than 3, see it as a line slice
            break
        else:
            raw_up-=1   
    while True:
        n = 0
        for each in imarray[raw_down]:
            if each==0:
                n+=1
        if n<=3:
            break
        else:
            raw_down+=1
    list_ref = word_analysis(imarray,raw_up,raw_down)
    #check_column(imarray,raw_up,raw_down,list_ref)
    try:
        order = 0
        column_right = 1
        column_left = 0
        for i in range(len(list_ref)-1):
            if list_ref[i]<=args[1]<=list_ref[i+1]:
                column_left = list_ref[i]
                column_right = list_ref[i+1]
                order = i
                break
        img2 = img1.crop((0,raw_up,len(imarray[0])-1,raw_down))
        text = pytesseract.image_to_string(img2, lang = 'eng')
        list_text = re.findall('\w+',text)
        w1 = list_text[order]
        img3 = img1.crop((column_left,raw_up,column_right,raw_down))
        w2 = pytesseract.image_to_string(img3, lang = 'eng')
        if is_similar(w1,w2):
            return w1
        elif len(w2)==0:
            return w1
        else:
            return w2
    except:
        try:
            img4 = img1.crop((column_left,raw_up,column_right,raw_down))
            w2 =  pytesseract.image_to_string(img4, lang = 'eng')
            return w2
        except:
            return 'choose again'
def motion(event):
    t1 = time.perf_counter()
    print(pointing_word(img,imarray,event.y,event.x))
    t2 = time.perf_counter()
    print('cost : ',t2-t1)
    return
master = tk.Tk()
master.title('This is a freaking test')
img = Image.open('img3.jpg')
imarray = img_to_array(img)
tkimg = ImageTk.PhotoImage(img) 
master.geometry('{}x{}'.format(*img.size))
pic = tk.Label(master, image = tkimg)
pic.pack(side = "bottom", fill = "both", expand = "yes") 
pic.bind('<Button>',motion)
# master.pack()
tk.mainloop()
"""print(pointing_word('img3.jpg',400,361))
raw_analysis(img_to_array('img1.jpg'))
t1 = time.perf_counter()
im = pointing_word('img1.jpg',500,361)
t2 = time.perf_counter()
print(t2-t1)
im.show()
text = pytesseract.image_to_string(im, lang='eng')
print(text)"""
