from collections import namedtuple

Word = namedtuple('Word', ['word', 'definitions', 'examples', 'pronunciation'])

"""
Word: A named tuple representing a looked-up word.

Attributes:

    word: a string saving the word.
    
    definitions: A list of definition of the word. Must have the same order with
        examples (see examples below).

    examples: A list of list of examples of the word, corresponding the
        definitions. Must have the same order with definitions (see examples
        below.)

    pronounciation: A string, which is the pronunciation of that word.

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

