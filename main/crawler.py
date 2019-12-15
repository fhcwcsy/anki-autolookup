from collections import namedtuple
import re
import requests
import urllib.request 
from bs4 import BeautifulSoup 
 
keepExamples = 2
Entry = namedtuple('Entry', 
        ['word', 'pos', 'pronunciation', 'definitions', 'examples'])

"""
Entry: A named tuple representing an entry in a dictionary of a looked-up word.

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

    w = Word('dynamic',

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

class LookupRequest:
    def __init__(self, word):
        self._word = word
        self._entries = None



    def onlineLookup(self):
        """
        Look up a word in the specified dictionary source. The word provided 
        must be found in the local wordlist. If the lookup fails, then return 
        a tuple of (word, None).
        
        Arguments: 
            word: the word to look up
            return: A tuple containing the word and its definition found
        """
            
        try:
            prefix = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/' 
            url = prefix + self._word 
            response = requests.get(url)
            print(response.status_code)
            soup = BeautifulSoup(response.text, "html.parser") 
            webEntries = soup.findAll('div', 'pr entry-body__el')
            self._entries = []
            for entry in webEntries:
                pronunciation = entry.find('span', 'us dpron-i').find('span', 'lpl-1').text
                pos = entry.find('span', 'pos dpos').text
                pronunciation = '/{}/'.format(
                        entry.find('span', 'ipa dipa lpr-2 lpl-1').text)
                definition_tags = entry.findAll('div', 'def-block ddef_block')
                definition_list = []
                example_list = []
                for dt in definition_tags:
                    if ((dt.parent.attrs['class'])[0] == 'phrase-body'):
                        continue
                    definition_list.append(
                            dt.find('span', 'trans dtrans dtrans-se').text)
                    example_list.append([t.text for t in dt.findAll(
                        'span', 'eg deg')][:keepExamples])
                self._entries.append(Entry(self._word, pos, pronunciation,
                    definition_list, example_list))
                    # print(t.parent.attrs)
                # print(len(definition_tags))
            print(self._entries)

        except Exception as e:
            raise e
     

if __name__ == "__main__":
    l = LookupRequest('record')
    l.onlineLookup()
