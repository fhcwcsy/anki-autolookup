# Copied from https://foosoft.net/projects/anki-connect/ 
import json
import urllib.request
from collections import namedtuple

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

        elif.result = self.response["result"]


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


if __name__ == "__main__":

    # check API version
    if Request("version").result != 6 :
        raise Exception("API version is not 6")
    
    #entries is a list of nametuples, which is stored in the attribute "_entries" of the class "LookupRequest"
    add_note(entries)
    print("done")


#entries格式：
#[entry(word='', pos='', pronunciation='', definitions=['', '', ''], examples=[[], [], []]), entry(...)]

