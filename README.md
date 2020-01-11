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

Below we lists detailed descriptions for each script.

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
 
##### Class Method description

**Public methods**

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

- `LookupRequest.export() `

**Private methods**: these methods should not be used and are only listed to
explain how they work (since we are asked to explain).

- `LookupRequest._directOnlineLookup([target, replace])`

### `imgrecog.py`

### `main.py`

### `wordlist_cls.py`

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
