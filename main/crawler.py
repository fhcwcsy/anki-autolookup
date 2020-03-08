# -*- coding: utf-8 -*-
"""
    anki-autolookup.crawler
    ~~~~~~~~~~~~~~~~~~~~~~~
    This file defines a namedtuple Entry to represent a dictionary entry, and a
    LookupRequest class to represent a lookup in Cambridge dictionary for each word.
    The required modules are:

    - collections
    - re (reqular expression)
    - requests
    - urllib
    - bs4 (BeautifulSoup)

"""

from collections import namedtuple
import re
import requests
import urllib.request 
from bs4 import BeautifulSoup 
 
KEEP_EXAMPLES = 2 # Maximum number of examples per entry

Entry = namedtuple('Entry', 
        ['word', 'pos', 'pronunciation', 'definitions', 'examples'])

"""Entry: A named tuple representing an entry in a dictionary of a looked-up word.

Attributes:

    word: a string saving the word.

    pos: part of speech. A string.
    
    pronounciation: A string, which is the pronunciation of that word.

    definitions: A list of definition of the word. Must have the same order with
        examples (see examples below).

    examples: A list of list of examples of the word, corresponding the
        definitions. Must have the same order with definitions (see examples
        below.)

Example:

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

"""

class LookupRequest(object):
    """A class to save a word, look it up and save its lookup results.

    Use

        w = LookupRequest('MyWord')

    to construct an object, then tell it to look up itself with

        w.onlineLookup()

    Finally, export the result, which is usually a list of Entry objects, with

        result = w.export()

    If the lookup failed, that is, no entry is found, then export will return
    None.

    Attributes:
        _word: A string. The word to be looked up (The original word inserted
            while constructing the object).

        _entries: A list of Entry objects. The entries found while looking up
            the word. Set to `None` before lookup.
     

    """
    
    def __init__(self, word):
        """Construct a LookupRequest instance with a word.

        Saves the word as an attribute without looking it up. 

        Args:
            word: the word to be looked up
        
        Returns:
            None
        
        Raises:
            None
        """

        self._word = word
        self._entries = None


    def onlineLookup(self):
        """Packed lookup method. Deals exceptions and British spellings.

        Calls self._direcOnlineLookup(), see its docstring for detailed
        description. If the lookup result turns out to be a "...的美式拼寫",
        then lookup again with the british spelling. If NoEntryFound exception
        was raised, then set self._entries to be None.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """

        try:
            self._cambridgeLookup()

            check_american = self._entries[0].definitions[0].find('的美式拼寫')

            if (check_american >= 0):

                # The british spelling as the target, and te original spelling 
                # will replace the british spelling.
                british_word = self._entries[0].definitions[0][1:check_american]
                self._cambridgeLookup(british_word, self._entries[0].word) 
        except Exception as e:
            try:
                self._dictionary_com_Lookup()
            except Exception as e:
                self._entries = None

    def _cambridgeLookup(self, target=None, replace=None):
        """Look up the word and saves a list of Entry objects to self._entries.

        Look up the word in Cambridge online dictionary and return a list of
        Entry objects.
        
        Arguments: 
            target: the word to look up. If the target is None, then lookup the
                word saved in self._word. Default value: None
            replace: Default value: None. If replace is not none, then the target
                word will be replaced with replace in the entries.

        return:
            None

        raises: 
            Raises NoEntryFound exception if the page is empty.
        """
        if target == None:
            target = self._word
            
        try:
            prefix = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/' 
            url = prefix + target 
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser") 
            webEntries = soup.findAll('div', 'pr entry-body__el')
            if len(webEntries) == 0:
                raise(Exception('NoEntryFound'))
            self._entries = []
            for entry in webEntries:
                if replace == None:
                    word = entry.find('span', 'hw dhw').text
                else:
                    word = self._word
                pronunciation = entry.find('span', 'us dpron-i').find(
                        'span', 'lpl-1').text
                pos = entry.find('span', 'pos dpos').text
                pronunciation = '/{}/'.format(
                        entry.find('span', 'ipa dipa lpr-2 lpl-1').text)
                definition_tags = entry.findAll('div', 'def-block ddef_block')
                definition_list = []
                example_list = []
                for dt in definition_tags:
                    if ((dt.parent.attrs['class'])[0] == 'phrase-body'):
                        continue
                    ch_def = dt.find('span', 'trans dtrans dtrans-se').text
                    eng_def = dt.find('div', 'def ddef_d db').text
                    def_text = ch_def + ' <br> ' + eng_def
                    definition_list.append(def_text)
                    example_single = [t.text for t in dt.findAll(
                        'span', 'eg deg')][:KEEP_EXAMPLES]
                    if replace:
                        for i in range(len(example_single)):
                            example_single[i] = example_single[i].replace(
                                    word, replace)
                    example_list.append(example_single)
                self._entries.append(Entry(word, pos, pronunciation,
                    definition_list, example_list))
            return True

        except Exception as e:
            # return False
            raise e

    def _dictionary_com_Lookup(self):
        prefix = 'https://www.dictionary.com/browse/' 
        url = prefix + self._word
        entry_list = list()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser") 
            # print(soup)
            webEntries = soup.findAll('div', 'css-1urpfgu e16867sm0')
            for entryBlock in webEntries:
                word_tag = entryBlock.find('h1', 'css-1jzk4d9 e1rg2mtf8')
                if word_tag == None:
                    continue
                word = word_tag.text

                # easy pronuncation
                # pronun = entryBlock.find('span',
                        # 'pron-spell-content css-z3mf2 evh0tcl2').text
                # IPA
                pronun = entryBlock.find('span',
                        'pron-ipa-content css-z3mf2 evh0tcl2').text

                pronun = re.sub('\\u2009', ' ', pronun)

                subEntries = entryBlock.findAll('section', 'css-pnw38j e1hk9ate0')
                for se in subEntries:
                    pos = se.find('span', 'luna-pos').text 
                    def_tags = se.findAll('div', 'e1q3nk1v3') 
                    defs = list()
                    exps = list()

                    for line in def_tags:
                        _def = line.text
                        _exp_tag = line.find('span', 'luna-example italic')
                        if _exp_tag != None:
                            _exp = _exp_tag.text
                            _def = _def[:_def.find(_exp)]
                        else:
                            _exp = ''
                        defs.append(_def)
                        exps.append([_exp])
                    entry_list.append(Entry(word, pos, pronun, defs, exps))
                break
            if len(entry_list):
                self._entries = entry_list
                return True
            else:
                raise Exception('EntryNotFound')
                return False

        except Exception as e:
            raise e
        
     
    def export(self):
        """Export the list of entries found.

        Args:
            None

        Returns:
            A list of Entry objects.

        Raises:
            None
        """

        return self._entries

if __name__ == "__main__":
    l = LookupRequest('undulate')
    l.onlineLookup()
    # l.onlineLookup()
    print(l.export()) 
