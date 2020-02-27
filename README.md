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

Use:

```{bash}
./start.sh
```

to start the program. Anki must be running in the background so the API can 
work. Select the deck you want to add cards to, then choose a method to add
words. Currently, three features are available:

- Word lookup: Simply type the words you want to lookup. The program will
record the word whenever you press `<Return>`. The words will be shown in the
wordlist on the right. You can uncheck the checkbuttons
beside a word you don't want to add to your deck. After the lookup finishes,
(the queue is empty), each word (if it is checked and **the lookup succeed**), the
program will generate a card to the deck.

- Article lookup: Paste an article to the textbox, then click `Lookup!`. The 
program will find the difficult words in the article and list them in the 
wordlist. The wordlist works the same way as the previous feature. For the
definition of _difficult words_, see the explanation of [`article_lookup.py`](https://github.com/fhcwcsy/anki-autolookup/blob/master/README.md#article_lookuppy).

- Image lookup: Choose a image (**must not be tilted or twisted or it will not
be accurate.** Some examples are provided in `./main/imgexample/`.) Click on the
words you want to lookup. The wordlist works the same way as the first feature.

Note that when you close the window of a feature, the main menu will show up
**after the queue is cleared.**

## Demonstration

[Youtube video](https://youtu.be/YkgdMulFnBs)

## File Description

```

.
+-- README.md: This documentation.
+-- start.sh: bash script to launch the program.
+-- main: Main scripts of the program.
|   +-- add_card.py: Functions to generate new cards and add to Anki.
|   +-- article_lookup.py: Lookup difficult words in an article.
|   +-- crawler.py: A cralwer to lookup words in Cambridge online dictionary.
|   +-- dic.xlsx: A spreadsheet with data about word usage in a variety of sources.
|   +-- imgrecog.py: The script for word lookup from images.
|   +-- main.py: Main menu GUI.
|   +-- wordlist_cls.py: The script defining the wordlist window.
|   +-- word_lookup.py: GUI for adding inserted words to Anki.
+-- presentation: Slides used (Tex and pdf files) for presentation in class.
|   +-- proposal.*: Slides for the proposal.
+-- trash: scripts that are no longer in use.

```

## Collaborators

- 張家翔 ([hsiang20](https://github.com/hsiang20)): API adaptor (`add_card.py`),
single word lookup feature GUI design (`word_lookup.py`), main menu GUI design
(`main.py`).

- 徐鼎翔 ([AlbertHsuNTUphys](https://github.com/AlbertHsuNTUphys)): Image 
recognition feature (`imgrecog`), article lookup GUI design (`article_lookup.py`).

- 王昊謙 ([fhcwcsy](https://github.com/fhcwcsy)): Wordlist window GUI design 
(`wordlist_cls`), crawler (`crawler.py`), speed enhancement in image recognition,
article lookup feature (my hw2), final modification in all files.
