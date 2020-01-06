# Copied from https://foosoft.net/projects/anki-connect/
# Please download the add-on "Allows empty first field" by the code: 49741504
import json
import urllib.request
from collections import namedtuple

Entry = namedtuple('Entry', 
        ['word', 'pos', 'pronunciation', 'definitions', 'examples'])
 
my_model = "anki_auto-lookup"
deckName = 'test'

class Request:

    def __init__(self, action, **params):
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


def add_note(wordinfo):
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
    #pos_len = len(pos)
    #pronunciation_len = len(pronunciation)
    #definitions_len = len(definition)
    #example_kind_len = len(example)
    #example_number = []
    #for i in range(example_kind_len):
        #example_number.append(len(example[i]))
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
    if my_model not in check.result:
        create_model = Request("createModel", modelName=my_model, 
                inOrderFields=inorderfields, 
                css=".card{font-family:Arial; background-color:white;}", 
                cardTemplates=[{"Front": "<font size='6'><b><center>{{word}}</center></b></font>", "Back":back}])
        

def new_deck_name(name):
    global deckName
    deckName = name



if __name__ == "__main__":

    # check API version
    if Request("version").result != 6 :
        raise Exception("API version is not 6")
    
        #print(new_request.result)


    entries = [Entry(word='colour', pos='noun', pronunciation='/ˈkʌl.ər/', definitions=['顏色', '色彩，色調', '顏料，染料', '紅潤的面色；血色，氣色', '趣味；風格；風味；色彩', '（人種的）膚色'], examples=[["What's your favourite color?", 'She wears a lot of bright colors.'], ['I think we need a bit of color in this room.', 'Red and yellow peppers give a little color to the sauce.'], ['I put my new green shirt in a hot wash and the color ran (= the color came out of the material).'], ['That walk has put some color in your cheeks.', 'I watched the color drain from her face as she heard the news.'], ['We added your story for a bit of local color.', "Michael was there so that added a bit of color to the evening's proceedings."], ['She felt she had not been given the job because of her color.', 'There should be no discrimination on the grounds of color.']]), Entry(word='colour', pos='adjective', pronunciation='/ˈkʌl.ər/', definitions=['（電視、照片、印刷）彩色的'], examples=[[]]), Entry(word='bark', pos='verb', pronunciation='/ˈkʌl.ər/', definitions=['變色；給…著色；使成為…色', '（因為尷尬而）臉紅', '影響（觀點）；使有偏見'], examples=[['Do you think he colors his hair?', 'He drew a heart and colored it red.'], [], ["I'm sure my views on marriage are colored by my parents' divorce.", "I'm trying not to let my judgment be colored by that one incident."]])] 
    create_model()
    add_note(entries)
    
    print("done")
    

#entries格式：
#[entry(word='', pos='', pronunciation='', definitions=['', '', ''], examples=[[], [], []]), entry(...)]

