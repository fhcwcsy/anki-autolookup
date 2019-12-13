class Word:

    """
    A class representing a word.
    
    Attributes:
    
        _word: a string saving the word.

        _definition: A dictionary with keys be the definitions of the word and
            a list of example sentences corresponding to that definition as
            values.
            
        _pronounciation: A string, which is the pronunciation of that word.

    Methods:

        Word.__init__(word, defdict, pronun): Constructor. Takes 3 arguments.
            word: the word it will be saving.
            defdict: A dictionary, with key be the definitions and a list of
                example sentences as values.
            pronun: A string. The pronunciation of the word.


        Word.word(): Takes no arguments and returns a string, which is the word
            this object saves.

        Word.definitions(): Takes no arguments and returns two list, with the
            first being the definitions, and the second being lists of example
            sentences. 

        Word.pronunciation(): Takes no arguments and returns the pronunciation
            of the word.

    Example:

        w = Word('dynamic', {'adjective. 思維活躍的；活潑的，充滿活力的，精力充沛的' : 
            ['She's young and dynamic and will be a great addition to the team.',
            'We need a dynamic expansion of trade with other countries.'], 
            'adjective. 不斷變化的；不斷發展的' : ['Business innovation is a
            dynamic process.', 'The situation is dynamic and may change at any
            time.']}, '/daɪˈnæm.ɪk/')

        w.word() = 'dynamic'

        w.definitions() = [
            'adjective. 思維活躍的；活潑的，充滿活力的，精力充沛的', 
            'adjective. 不斷變化的；不斷發展的'
            ], [
            ['She's young and dynamic and will be a great addition to the team.',
            'We need a dynamic expansion of trade with other countries.'], 
            ['Business innovation is a dynamic process.', 'The situation is
            dynamic and may change at any time.']
            ]
        
        w.pronunciation() = '/daɪˈnæm.ɪk/'

    """

    def __init__(self, word, defdict, pronun):
        self._word = word
        self._definition = defdict
        self._pronounciation = pronun

    def word(self):
        return self._word
        
    def definitions(self):
        return self._definition.keys(), self._definition.values()

    def pronunciation(self):
        return self._pronounciation

