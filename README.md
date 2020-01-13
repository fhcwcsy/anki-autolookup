# Anki Autolookup

This is a final project from a programming course. It may not be maintained, but
feel free to contact us if you want to contribute or maintain this project. 

## Table of Contents

- [Anki Autolookup](#anki-autolookup)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Demonstration](#demonstration)
  * [File Description](#file-description)
    + [`add_card.py`](https://github.com/fhcwcsy/anki-autolookup/blob/master/README.md#add_cardpy)
    + [`article_lookup.py`](https://github.com/fhcwcsy/anki-autolookup/blob/master/README.md#article_lookuppy)
    + [`cralwer.py`](https://github.com/fhcwcsy/anki-autolookup/blob/master/README.md#cralwerpy)
    + [`imgrecog.py`](https://github.com/fhcwcsy/anki-autolookup/blob/master/README.md#imgrecogpy)
    + [`main.py`](https://github.com/fhcwcsy/anki-autolookup/blob/master/README.md#mainpy)
    + [`wordlist_cls.py`](https://github.com/fhcwcsy/anki-autolookup/blob/master/README.md#wordlist_clspy)
    + [`word_lookup.py`](https://github.com/fhcwcsy/anki-autolookup/blob/master/README.md#word_lookuppy)
  * [Collaborators](#collaborators) 

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
|   +-- article_lookup.py: Lookup difficult words in an article.
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

This program will create a lookup window where the user can enter/paste an article 
and choose the difficulty of words he wants to be looked up. The program will 
find the words in the article that match the requirements and list in the wordlist
window on his right. Then, user can choose the words he want to add to anki.

The _difficulty_ of a word is defined as follows: We use a wordlist from [NGSL](http://www.newgeneralservicelist.org/),
which contains the words used in fictions, journals, TV subtitles, etc., and
their times of being used. Hence, the difficulties of a word is defined by the
frequency of being used. If a word is more oftenly used, it is considered to be
less difficult, and vice versa. If a word is not in the list, it is considered 
to be too difficult ore rarely used for a foreign English learner to learn. The
frequency used in this program is normalized by dividing the actual count of
usage by the number of times used of the most frequently used word (so the
frequency is between 0 and 1). This program reads the text paste in the textbox,
determine the difficulty of each word by looking up in the local wordlist, then
lookup each word in the Cambridge dictionary. 

The required modules are:

- `tkinter`
- `re` (regular expression)
- `openpyxl` 

Below we list all the classes in this file.

#### ArticleRecognitionWindow

This is the main window of the feature.

##### Attributes

- difficulty: The (normalized) maximum difficulty of the word to be looked up. 
The lower this value is, the less word (keeping only the most difficult ones)
will be looked up.

##### Class Methods

- `__init__(self)`

Create two windows. 

One is `_inputWindow` where the users enter the article and determine the 
difficulty of words they want to be looked up.
    
The other is `_wordwindow` where we show the the difficult words we find in the
article. Users can select which words they want to make vocabulary cards here.

    Args:
		None
    
    Return:
		None
            
    Raise:
		None

- `lookup()`

This function will first get the difficulty users set. Use it to find the 
difficult words in the article, and add it to the `_wordwindow`.

    Args:
		None
    
    Return:
		None
    
    Raise:
		raise Exception('InvalidDifficulty') if self.difficulty is not 
			between 0 and 1.

- `_quitwindow()`

Destroy/quit the windows after using it.

    Args:
		None
            
    Return:
		None
            
    Raise:
		None

- `_getWordlist()`

Read the excel sheet (the local dictionary with frequencies of the words)
and convert it into a dictinary with the key being the words and and 
the value being its `frequency/max_frequency`.
 

	Args:
        None

	Return: 
        A dictionary

	Raise:
        None

- `_getArticle(text)`

Read the text, cut it into words, then add them into a set and return.

    Args:
		text: The article we want to anaylze.
            
    Return: 
		A set containing the words.
    
    Raise:
		None

- `_dictLookup(word, d)`

Local wordlist lookup. Check if the word is in the wordlist and get its 
frequency. Also check the stripped words if the word matches any common suffixes.

    Args:
		word: the word to look up
		d: The dictionary to look up
    
    Return: 
		If any result is found, then return a tuple of (word, frequency).
		If the word (or any of the stripped version) is not in the list, then 
		return None.

    Raise:
		None

- `_setLookup(s, dictionary)`

Look up each word in the set in the local wordlist. If the word is found and its
frequency is below the self.difficulty, then recognize it as difficult word. 
Stopwords are removed.

    Args:
		s: a set containing the words to be looked up.
		dictionary: the dictionary with the key be the words and the value be 
		its frequency.
		
    Return: 
		a list containing the difficult words found in the local wordlist.

    Raise:
		None

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

- `__init__(word)`

Construct a LookupRequest instance with a word. Saves the word as an attribute
without looking it up. 

	Args:
		word: the word to be looked up

	Returns:
		None

	Raises:
		None
 

- `onlineLookup()`

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
 

- `export() `

Export the list of entries found.

	Args:
		None

	Returns:
		A list of Entry objects.

	Raises:
		None

- `_directOnlineLookup([target=None, replace=None])`

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

This file can lookup words from an image. The user select a picture, then it 
will be shown in a window. When the user click on the word in the picture, this
program will attempt to recognize the word and generate the vocabulary card. 
Note that the picture must be very well taken so that the lines are not tilted
or bent too much. Some examples are provided in `/main/imgexample/`. The required 
modules are:

-  PIL
-  numpy
-  pytesseract
-  re
-  tkinter

Below we list all classes we used in this file.

#### TextPicture

A picture containing text to be recognized.

##### Constants:
- `_BNW_THRESHOLD`

When the gray scale number of a pixel is smaller than this constant, it will
be recognized as a white pixel and set to 0. Otherwise, it will be
recognized as a black pixel and set to 1.

- `_LINE_THRESHOLD`

 When the number of black pixels in a raw is less than this number,
it will be recognized as a white line.
 
- `__SPACE_THRESHOLD`

When the black pixels in a column is less than this constant,
it will be considered as a white column.
 
##### Attributes:

No public attributes.

##### Class Methods:
- `_is_similar(s1,s2)`

Determine whether two words s1 and s2 are similar or not.

We would compare the length and the characters in them to determine whether they are similar or not.
	Args:
		s1, s2: two strings to be compared.
			
	Return:
			True: if they are similar.
			False: if they are not.

	Raises:
		None

- `_extractLine(lineUpperBound, lineLowerBound)`

This method will analyze the a region which is defined by
lineUpperBound and lineLowerBound. This region should contain the line
to be analyzed.

We will first sum up vertically to detect the white column. If the
number of black pixels in a column is less than `_SPACE_THRESHOLD`, we
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
 

- `_bindEvent(event)`:

When the event is occured, we will return the word on the position (event.x, event.y)

    Args:
		event: The event that triggers the function recognizeWord.
            
    Return:
		The word recognized at position (event.x, event.y)
    
    Raise:
		None

#### ImgRecognitionWindow

Defines the window showing the image. The user clicks
on words they want to look up and the word will be listed in the wordlist 
on the right. This class inherit the class `TextPicture`

##### Class Methods

- `__init__(self)`

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
 

- `_quitwindow()`

Destroy/quit the windows.

    Args:
		None
            
    Return:
		None
            
    Raise:
		None

- `bindEvent(event)`
    
When the event occured, We will detect the word users click and add it to the
`_wordWindow`

    Args:
		None
            
    Return:
		None
            
    Raise:
		None

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

- `__init__(master, quitFunc [, **kwargs])`

Construct a modified tk.Frame object with scrollbar and word checklist.

Constructor. Inherit the Frame class from tk, while adding a scrollbar,
and word listing feature. Takes all arguments as tk.Frame.

	Args:
		same as tk.Frame.

	Return:
		None

	Raises:
		None
 

- `newWord(word)`

Add new words

function to add new word. load the word in to the queue, then the method
`_lookupThreading` will look them up in the background.

	Args:
		word: The word to be added.

	Returns:
		None

	Raises:
		None
 
- `_updateStatus()`

Update the status label to indicate the queue length.

- `_lookupThreading()`

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
 
- `_quitAndAdd()`

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
 

- `_set_scrollregion([event=None])`

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
article lookup feature (my hw2), final modification in all files.
