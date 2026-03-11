token_types = (
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
    #('NUMBER', '0') # need to figure this one out - example: timestamps, effect values
    ('LITERAL', 'x') # need to figure this one out - example: variable filepaths (user defined)
    ('IDENTIFIER', 'x'), # need to figure this one out - example: video variable name (user defined)
    ('END', '') # end of text
)

token_map = dict(token_types)

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
        self.current_char = None

    def forward(self):
        self.pos += 1
        if self.current_char < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_space(self):
        while self.current_char.isspace() and self.current_char is not None:
            self.forward()

    def build_num(self):
        num = ''
        while self.current_char.isdigit() and self.current_char is not None:
            num += self.current_char
            self.forward()
        return Token('NUMBER', int(num)) # may need to change NUMBER to search through token array or soemthing?
    
    def get_pair(self, key):
        for token in token_types:
            if token[0] == key:
                return token
    
    def build_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_space()
            elif self.current_char.isdigit():
                tokens.append(self.build_num())
            elif self.current_char == token_map['ASSIGN']:
                tokens.append(Token(self.get_pair('ASSIGN')))

        tokens.append(Token(self.get_pair('END')))
        return tokens
    

if __name__ == '__main__': # Test usage
    text_input = 'video = image + audio'
    lex = Lexer(text_input)
    token_stream = lex.build_tokens()
    print(token_stream)