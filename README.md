# Anki Autolookup

This is a final project from a programming course. It may not be maintained, but
feel free to contact us if you want to contribute or maintain this project. 

## Installation

**This program is only tested on Ubuntu 19.04 and Ubuntu 19.10**. To use it you need
to clone the project first:
```{bash}
git clone https://github.com/fhcwcsy/anki-autolookup.git
```
You will also need an additional module [**Tesseract**](https://github.com/tesseract-ocr/tesseract/blob/master/README.md),
please follow the installation there. For Ubuntu users, all you need to do is:
```{bash}
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```
Then:
```{bash}
pip install pytesseract 
```

You will also need two Anki plugins: `Allows empty first field (during adding
and import)` and `AnkiConnect`. Add them by clicking `Tools - Add-ons` in Anki,
then use `46741504` and `2055492159` to add the plugins.  


## Usage

```{bash}
./start.sh
```

## Demonstration

[Youtube video](https://youtu.be/YkgdMulFnBs)

## File Description

```

.
+-- README.md: This documentation.
+-- start.sh: bash script to launch the program.
+-- main: Main scripts of the program.
|   +-- add_card.py
|   +-- article_lookup.py
|   +-- crawler.py: A cralwer to lookup words in Cambridge online dictionary.
|   +-- dic.xlsx: A spreadsheet with data about word usage in a variety of sources.
|   +-- imgrecog.py: The script for word lookup from images.
|   +-- main.py
|   +-- wordlist_cls.py: The script defining the wordlist window.
|   +-- word_lookup.py:
+-- presentation: Slides used (Tex and pdf files) for presentation in class.
|   +-- proposal.*: Slides for the proposal.
+-- trash: scripts that are no longer in use.

```

Below we lists detailed descriptions for each script. **All of these are copied
from the docstrings. You can simply skip these and read the codes if you want
to understand the program. They are only listed because we are asked to do so.**

### `add_card.py`

### `article_lookup.py`

### `cralwer.py`

This file defines a namedtuple Entry to represent a dictionary entry, and a
LookupRequest class to represent a lookup in [Cambridge Dictionary](https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/)
for each word. The required modules are:

- collections
- re (reqular expression)
- requests
- urllib
- bs4 (BeautifulSoup)

Below we list all the classes defined in this file.

#### Entry

A namedtuple representing an entry in a dictionary of a looked-up word.

##### Usage:

```
Entry(word, partOfSpeech, pronunciation, listOfDefinitions, listOfExamples)
```

##### Attributes:

- word: a string saving the word.

- pos: part of speech. A string.

- pronounciation: A string, which is the pronunciation of that word.

- definitions: A list of definition of the word. Must have the same order with
examples (see examples below).

- examples: A list of list of examples of the word, corresponding the definitions. 
Must have the same order with definitions (see examples below.)

##### Example:

```
w = Entry('dynamic',

	['adjective. 思維活躍的；活潑的，充滿活力的，精力充沛的',
	'adjective. 不斷變化的；不斷發展的'], 

	[['She's young and dynamic and will be a great addition to the team.',
	'We need a dynamic expansion of trade with other countries.'], 
	['Business innovation is a dynamic process.', 
	'The situation is dynamic and may change at any time.']],

	'/daɪˈnæm.ɪk/')

w.word = 'dynamic'

w.definitions = 
	['adjective. 思維活躍的；活潑的，充滿活力的，精力充沛的', 
	'adjective. 不斷變化的；不斷發展的']

w.examples = 
	[['She's young and dynamic and will be a great addition to the team.',
	'We need a dynamic expansion of trade with other countries.'], 
	['Business innovation is a dynamic process.', 'The situation is
	dynamic and may change at any time.']]

w.pronunciation() = '/daɪˈnæm.ɪk/'
```

#### LookupRequest 

A class to save a word, look it up and save its lookup results.

##### Usage

To construct an object, use:
```
w = LookupRequest('MyWord')
```

To tell it to look up itself, use
```
w.onlineLookup()
```
Finally, export the result, which is usually a list of Entry objects, with
```
result = w.export()
```
If the lookup failed, that is, no entry is found, then export will return
`None`.

##### Attributes

No public attributes.
 
##### Class Methods

- `LookupRequest.__init__(word)`

Construct a LookupRequest instance with a word. Saves the word as an attribute
without looking it up. 

	Args:
		word: the word to be looked up

	Returns:
		None

	Raises:
		None
 

- `LookupRequest.onlineLookup()`

Packed lookup method. Deals exceptions and British spellings.

Calls `self._direcOnlineLookup()`, see its explanation below for detailed
description. If the lookup result turns out to be a "...的美式拼寫",
then lookup again with the british spelling. If NoEntryFound exception
was raised, then set `self._entries` to be None.

	Args:
		None

	Returns:
		None

	Raises:
		None
 

- `LookupRequest.export() `

Export the list of entries found.

	Args:
		None

	Returns:
		A list of Entry objects.

	Raises:
		None

- `LookupRequest._directOnlineLookup([target=None, replace=None])`

Look up the word and saves a list of Entry objects to `self._entries`.

Look up the word in Cambridge online dictionary and return a list of
Entry objects. 

	Args: 
		target: the word to look up. If the target is None, then lookup the
			word saved in self._word. Default value: None
		replace: Default value: None. If replace is not none, then the target
			word will be replaced with replace in the entries.

	return:
		None

	raises: 
		Raises NoEntryFound exception if the page is empty.

### `imgrecog.py`

This file will create a window .Users can select a picture file, and it would be shown in this window. When users click on the word of it, this program will recognize the word and generate the vocabulary card. The required modules are:

-  PIL
-  numpy
-  pytesseract
-  re
-  tkinter

Below we list all classes we used in this file.

#### Text Picture
A picture containing text to be recognized.
##### Constants:
- _BNW_THRESHOLD: The constant which will be used to process the picture(see imgArray below). When the number is larger than it, we will detect it as white and set it to be 0. Otherwise, we will detect is as black and set it to be 1. We set it to be 140 here.
- LINE_THRESHOLD: When the black pixels in a raw is less than this constant, we will detect it as a white line. Here we set it to be 3.
- SPACE_THRESHOLD: When the black pixels in a column is less than it, we detect it as a white column. Here we set it to be 2. 
##### Attributes:
- originalImg: The target picture to be recognized.
- imgArray: The array of the image, which is processed a little bit to make it more easliy to analyze. (Turn the array to be 0 and 1 only. 0 means white, while 1 means black)  
- processedImg: The processed image mentioned above.
- height: The height of the picture.
- width: The width of the picture.
- _horizontalSum: The number of black points of each horiaontal raw of the picture.
##### Class Methods:
- `is_similar(s1,s2)`
Determine whether s1 and s2 are similar or not.
We would compare the length and the characters in them to determine whether they are similar or not.
```
Args:
	s1, s2: two strings to be compared.
        
Return:
        True: if they are similar.
        False: if they are not.

Raises:
	None
```
- `_extractLine(lineUpperBound, lineLowerBound)`
This method will analyze the interest region which is given by lineUpperBound and lineLowerBound. And this interest region is actually a subset of the imgarray.
We will first sum up vertically to detect the white column. If the number of black pixels in a column is less than SPACE_THRESHOLD, we recognize it as a white column. Find the wider white column to be the divide of two words. And then we return a list of index of divide of words. 
```
Args:
        lineUpperBound: The upper bound of raw of the interest region.
        lineLowerBound: The lower bound of raw of the interest region.
        
Return:
        wordIndices: a list of index of divide of words.

Raise:
        Exception: raise e
```

### `main.py`

### `wordlist_cls.py`

This file defines the WordlistWindow class, which is the window with all the
word added to be looked up. It uses threading module to lookup in the
background.
 
Below we list all the classes defined in this file.

#### WordlistWindow

A class defining the frame listing all the words to be added.
    
The design of this class is based on the answer [here](https://stackoverflow.com/questions/23483629/dynamically-adding-checkboxes-into-scrollable-frame)

This class inherit tk.Frame. Initiate the window by  constructing an
instance as a normal tk.Frame:

```
	w = WordlistWindow(master, quitFunc)
```

Then pack/grid to show the frame. Use

```
	w.newWord('MyWord')
```

to add a new word. The word should pop up in the list immediately, unless it
is already in the list. A lookup process will be initiated in the background
once the object is constructed. Each word added with `newWord()` method will
be added to a queue, and will be looked up one by one in the background with
threading module. The words added to the list should have its checkbutton 
checked by default. The user can click on the "done" button to quit and 
`quitFunc()` will be called, which can be used to close the window.

##### Attributes

- vscrollbar: The vertical tk.Scrollbar object on the right.

- canvas: The tk.Canvas in the background of the frame.

- interior: a tk.Frame object that everything lie on.
 
##### Class Methods

- `WordlistWindow.__init__(master, quitFunc [, **kwargs])`

Construct a modified tk.Frame object with scrollbar and word checklist.

Constructor. Inherit the Frame class from tk, while adding a scrollbar,
and word listing feature. Takes all arguments as tk.Frame.

	Args:
		same as tk.Frame.

	Return:
		None

	Raises:
		None
 

- `WordlistWindow.newWord(word)`

Add new words

function to add new word. load the word in to the queue, then the method
`_lookupThreading` will look them up in the background.

	Args:
		word: The word to be added.

	Returns:
		None

	Raises:
		None
 
- `WordlistWindow._updateStatus()`

Update the status label to indicate the queue length.

- `WordlistWindow._lookupThreading()`

Look up words in `self._queue` in the background.

Uses threading module to implement multitasking, so it will continue to
lookup words (the speed depends on the internet speed) while the user
input words (the speed depends on CPU and GPU).

	Args:
		None

	Returns:
		None

	Raises:
		None
 
- `WordlistWindow._quitAndAdd()`

Add the words checked and quit.

Called when the user hit the "quit" button. The function wait until all
cards have been looked up (the queue is empty), then add all cards to
deck, and finally quit the window. 

	Args:
		None

	Returns:
		None

	Raises:
		None
 

- `WordlistWindow._set_scrollregion([event=None])`

Update scroll region of the scrollbar.
 

### `word_lookup.py`

## Collaborators

- 張家翔 ([hsiang20](https://github.com/hsiang20)): API adaptor (`add_card.py`),
single word lookup feature GUI design (`word_lookup.py`), main menu GUI design
(`main.py`).

- 徐鼎翔 ([AlbertHsuNTUphys](https://github.com/AlbertHsuNTUphys)): Image 
recognition feature (`imgrecog`), article lookup GUI design (`article_lookup.py`).

- 王昊謙 ([fhcwcsy](https://github.com/fhcwcsy)): Wordlist window GUI design 
(`wordlist_cls`), crawler (`crawler.py`), speed enhancement in image recognition,
final modification in all files.
