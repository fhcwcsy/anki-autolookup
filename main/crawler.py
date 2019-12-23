from collections import namedtuple
import re
import requests
import urllib.request 
from bs4 import BeautifulSoup
import json
import urllib.request
 
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
        Packed lookup method. Deals with special cases.
        """

        self._directOnlineLookup()

        # American English spelling
        if self._entries[0].definitions[0][-6:] == '的美式拼寫）':

            self._directOnlineLookup(self._entries[0].definitions[0][1:-6], self._entries[0].word)

    def _directOnlineLookup(self, target=None, replace=None):
        """
        Look up the word in Cambridge online dictionary and return a list of
            Entry objects. If the word is found to be spelled in American
            English, the function rerun to get the correct meaning.
        
        Arguments: 
            word: the word to look up
        return: A list of Entry objects
        """
        if target == None:
            target = self._word
            
        try:
            prefix = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/' 
            url = prefix + target 
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser") 
            webEntries = soup.findAll('div', 'pr entry-body__el')
            self._entries = []
            for entry in webEntries:
                word = entry.find('span', 'hw dhw').text
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
                    def_text = dt.find('span', 'trans dtrans dtrans-se').text
                    definition_list.append(def_text)
                    example_single = [t.text for t in dt.findAll(
                        'span', 'eg deg')][:keepExamples]
                    if replace:
                        for i in range(len(example_single)):
                            example_single[i] = example_single[i].replace(word, replace)
                    example_list.append(example_single)
                self._entries.append(Entry(word, pos, pronunciation,
                    definition_list, example_list))

        except Exception as e:
            raise e
     
    def export(self):
        return self._entries



class Request:

    def __init__( self, action, **params):
        self.action = action
        self.request = {"action": action, "params": params, "version": 6} 
        self.response = None
        self.result = None
        self.invoke()

    def invoke(self):
        requestJson = json.dumps(self.request).encode('utf-8')
        self.response = json.load(urllib.request.urlopen(urllib.request.Request("http://localhost:8765", requestJson)))

        if len(self.response) != 2:
            raise Exception("response has an unexpected number of fields")
        
        if "error" not in self.response:
            raise Exception("response is missing required error field")

        if "result" not in self.response:
            raise Exception("response is missing required result field")

        if self.response['error'] is not None:
            raise Exception(self.response['error'])

        self.result = self.response["result"]
        # TODO: return value undefined!!

def add_note(wordinfo):
    front = ''
    for entry in wordinfo:
        word = entry.word
        front += entry.pos + '\n'
        front += entry.pronunciation + '\n'
        for defi in entry.definitions:
            front += defi + '\n'
        for ex in entry.examples:
            try:
                front += ex[0] + '\n'
            except:
                pass
        
    new_request = Request("addNote", note = {"deckName":"test", "modelName":"Basic", "fields":{"Front":word, "Back":front}, "options":{"allowDuplicate":False}, "tags":["yomichan"]})
 


if __name__ == "__main__":
    l = LookupRequest('color')
    l.onlineLookup()
    

    add_note(l._entries)
    
