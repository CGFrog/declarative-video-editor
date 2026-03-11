tokens = (
    # OPERATORS
    ('ASSIGN', '='),         # assignment                
    ('UNION', '+'),                 # union                    
    ('FUNC_COMP', '|>'),             # function composition 

    # TYPES
    ('VIDEO', 'video'), 
    ('AUDIO', 'audio'), 
    ('IMAGE', 'image'), 

    # EFFECTS
    ('BLUR', 'blur'), # blur
    ('SATURATION', 'saturation'), # saturation
    ('CHROMA', 'chroma'), # chroma key

    # BRACKETS & MISC.
    ('LPAREN', '('),
    ('RPAREN', ')'),
    ('QOUTES', '"'),
    ('COMMA', ','),
    ('COLON', ':'),
    ('NUMBER', '0') # need to figure this one out - example: timestamps, effect values
    ('LITERAL', 'x') # need to figure this one out - example: variable filepaths (user defined)
    ('IDENTIFIER', 'x') # need to figure this one out - example: video variable name (user defined)
)

class Token():

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toString(self):
        return f"Token({self.key}, {self.value})"

class Lexer():

    def __init__(self, text):
        self.text = text
        self.pos = 0