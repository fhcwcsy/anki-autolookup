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
        No public attributes.

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
        """Packed lookup method. Deals with special cases.

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
            self._directOnlineLookup()

            # American English spelling
            if (len(self._entries[0].definitions[0]) > 6
                    and self._entries[0].definitions[0][-6:] == '的美式拼寫）'):

                # The british spelling as the target, and te original spelling 
                # will replace the british spelling.
                self._directOnlineLookup(self._entries[0].definitions[0][1:-6],
                        self._entries[0].word) 
        except Exception as e:
            self._entries = None

    def _directOnlineLookup(self, target=None, replace=None):
        """Look up the word and saves a list of Entry objects to self._entries.

        Look up the word in Cambridge online dictionary and return a list of
        Entry objects. If the word is found to be spelled in American English,
        the function rerun to get the correct meaning.
        
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
                    def_text = dt.find('span', 'trans dtrans dtrans-se').text
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
    l = LookupRequest('python')
    l.onlineLookup()
    print(l.export()) 
