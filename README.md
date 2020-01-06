# Anki Autolookup

**This is an unfinished project and should not be used yet.**

## Installation

This program is only tested on Ubuntu 19.04 and Ubuntu 19.10. To use it you need
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
|   +-- gui.py
|   +-- imgrecog.py: The script for word lookup from images.
|   +-- ui.py:
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

### `gui.py`

### `imgrecog.py`

### `ui.py`

### `wordlist_cls.py`

### `word_lookup.py`

## Contribution

