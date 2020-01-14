"""
This file defines a Request class and three functions (add_note, 
create_model, new_deck_name), to connect to anki API and converts the 
information obtained by `crawler.py` to cards in anki.

The required modules are:

- json
- urllib.request
- collections (namedtuple)
"""

from collections import namedtuple
import json
import urllib.request

Entry = namedtuple('Entry', 
        ['word', 'pos', 'pronunciation', 'definitions', 'examples'])
my_model = "anki_auto-lookup"
deckName = None
"""
    Entry: The same as Entry in `crawler.py`.
    my_model: The model name we want to create in anki. This name can not be 
    the same as the default ones, such as "Basic", "Basic(and reversed card)", 
    and "Cloze".
    deckName: Used to stored the list of user's deck names.
"""
class Request:
    """
    A class to connect with anki API. This class is mainly copied from the 
    anki-connect website:
    https://foosoft.net/projects/anki-connect/
    
    Attribute:
        _action: A string, the action users want to do with anki API.
        _request: A dictionary, the request to anki API.
        _response: A dictionary, the response returned by anki API, associated with 
        the request. Contains "result" and "error".
        _result: The result part of _response.

    """
    def __init__(self, action, **params):
        """Constructor of the class.

        Args:
            action: The action users want to do with anki API.
            params: The other necessary information associated with the action.

        Returns:
            None
        
        Raises:
            None
        """ 
        self._action = action
        self._request = {"action": action, "params": params, "version": 6} 
        self._response = None
        self._result = None
        self._invoke()

    def _invoke(self):
        """
        This method connects with anki API and check if there is any mistake. If 
        not, put the response in the attribute _response.
        Args:
            None

        Returns:
            None
        
        Raises:
            Raise Exception ("response has an unexpected number of fields") if 
                the anki-connect system returned an invalid response.
            Raise Exception ("response is missing required error field") if the 
                anki-connect system didn't returned error field.
            Raise Exception ("response is missing required result field") if the 
                anki-connect system didn't returned result field.
            Rasie Exception (self._response) if there exists errors in the 
                returned response.
        """
        requestJson = json.dumps(self._request).encode('utf-8')
        self._response = json.load(urllib.request.urlopen(urllib.request.Request("http://localhost:8765", requestJson)))
        if len(self._response) != 2:
            raise Exception("response has an unexpected number of fields")
        
        if "error" not in self._response:
            raise Exception("response is missing required error field")

        if "result" not in self._response:
            raise Exception("response is missing required result field")

        if self._response['error'] is not None:
            raise Exception(self._response['error'])

        self._result = self._response["result"]


def add_note(wordinfo):
    """
    This function calls `Request`, using "addnote" as action, "deckName" as 
    deckname, "my_model" as modelname, "fields" as field.
    "deckname" is indicated by users. "my_model" is created by the function 
    `create_model`. "fields" is made by the information got by `crawler.py`.
    This function rearrange the information got by `crawler` to fit the model, 
    then create a new card in anki.

    Args:
        wordinfo: A list of Entry objects obtained by the crawler. The format is 
        demonstrated in `crawler.py`.

    Returns:
        None

    Raises:
        None 
    """
    global my_model
    global deckName
    i = 0
    pos = [''] * 5
    pronunciation = [''] * 5
    definitions = [''] * 5
    examples = []
    for i in range(5):
        examples.append([])
    
    i = 0
    for entry in wordinfo:
        word = entry.word
        pos[i] = entry.pos
        pronunciation[i] = entry.pronunciation
        for defi in entry.definitions:
            definitions[i] += defi + ', '
        try:
            if definitions[i][-2:] == ', ':
                definitions[i] = definitions[i][:-2]
        except:
            pass
        for ex in entry.examples:
            for exs in ex:
                examples[i].append(exs)    
        i += 1
    
    fields = {"word":word}
    for i in range(5):
        field = "pos" + str(i)
        fields[field] = pos[i]
        field = "pronunciation" + str(i)
        fields[field] = pronunciation[i]
        field = "definitions" + str(i)
        fields[field] = definitions[i]
        j = 0
        for j in range(10):
            field = "examples" + str(i) + "_" + str(j) 
            try:
                fields[field] = examples[i][j]
            except:
                fields[field] = ' '
                
    add_card = Request("addNote", note={"deckName": deckName, "modelName": my_model, "fields":fields, "tags":""}) 


def create_model():
    """
    This function creates a card model using html. Using class `Request` and 
    action "modelName" to check if "my_model" is one of the user's deck name. 
    If not, create one using class `Request` and action "createModel".

    Args:
        None

    Returns:
        None

    Raises:
        None 
    """
    global my_model
    check = Request("modelNames")
    inorderfields = ["word"]
    back = "{{FrontSide}}<hr>"
    for i in range(5):
        inorderfields.append("pos"+str(i))
        inorderfields.append("pronunciation"+str(i))
        inorderfields.append("definitions"+str(i))
        back += "<center><strong><font size='5', color=darkred>" + "{{pos" + str(i) + "}}</strong></font><br>{{pronunciation" + str(i) + "}}<br><font size='3', color=kblue><strong>{{definitions" + str(i) + "}}</strong></font></center>"
        for j in range(10):
            inorderfields.append("examples"+str(i)+"_"+str(j)) 
            back += "{{examples" + str(i) + "_" + str(j) + "}}<br>"
    if my_model not in check._result:
        create_model = Request("createModel", modelName=my_model, 
                inOrderFields=inorderfields, 
                css=".card{font-family:Arial; background-color:white;}", 
                cardTemplates=[{"Front": "<font size='6'><b><center>{{word}}</center></b></font>", "Back":back}])
        

def _new_deck_name(name):
    """
    Update "deckName". If "name" is an empty string as default, return None.

    Args:
        name: A list, the deck names in the user's anki.

    Returns:
        If name is '' (default), return None.
        If name is a list, return True.

    Raises:
        None 
    """
    global deckName
    if name == '':
        return None
    deckName = name
    return True



if __name__ == "__main__":

    # check API version
    if Request("version")._result != 6 :
        raise Exception("API version is not 6")
    
        #print(new_request._result)


    # entries = [Entry(word='colour', pos='noun', pronunciation='/ˈkʌl.ər/', definitions=['顏色', '色彩，色調', '顏料，染料', '紅潤的面色；血色，氣色', '趣味；風格；風味；色彩', '（人種的）膚色'], examples=[["What's your favourite color?", 'She wears a lot of bright colors.'], ['I think we need a bit of color in this room.', 'Red and yellow peppers give a little color to the sauce.'], ['I put my new green shirt in a hot wash and the color ran (= the color came out of the material).'], ['That walk has put some color in your cheeks.', 'I watched the color drain from her face as she heard the news.'], ['We added your story for a bit of local color.', "Michael was there so that added a bit of color to the evening's proceedings."], ['She felt she had not been given the job because of her color.', 'There should be no discrimination on the grounds of color.']]), Entry(word='colour', pos='adjective', pronunciation='/ˈkʌl.ər/', definitions=['（電視、照片、印刷）彩色的'], examples=[[]]), Entry(word='bark', pos='verb', pronunciation='/ˈkʌl.ər/', definitions=['變色；給…著色；使成為…色', '（因為尷尬而）臉紅', '影響（觀點）；使有偏見'], examples=[['Do you think he colors his hair?', 'He drew a heart and colored it red.'], [], ["I'm sure my views on marriage are colored by my parents' divorce.", "I'm trying not to let my judgment be colored by that one incident."]])] 
    # create_model()
    # add_note(entries)

    r = Request('deckNames')
    print(r._response)
    print("done")
    
