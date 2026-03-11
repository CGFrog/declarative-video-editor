token_types = (
    # OPERATORS
    ('ASSIGN', '='),         # assignment                
    ('UNION', '+'),                 # union                    
    ('FUNC_COMP', '|>'),             # function composition 

    # TYPES
    #('VIDEO', 'video'), 
    #('AUDIO', 'audio'), 
    #('IMAGE', 'image'), 

    # EFFECTS
    #('BLUR', 'blur'), # blur
    #('SATURATION', 'saturation'), # saturation
    #('CHROMA', 'chroma'), # chroma key

    # BRACKETS & MISC.
    ('LPAREN', '('),
    ('RPAREN', ')'),
    ('QOUTES', '"'),
    ('COMMA', ','),
    ('COLON', ':')#,
    #('NUMBER', '0') # need to figure this one out - example: timestamps, effect values
    #('LITERAL', 'x'), # need to figure this one out - example: variable filepaths (user defined)
    #('IDENTIFIER', 'x'), # need to figure this one out - example: video variable name (user defined)
    #('END', '') # end of text
)

token_map = dict(token_types)
#print(token_map)
#symbols = list(token_map.values())
#print(symbols)

class Token():

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toString(self):
        return f"Token({self.key}, {self.value})"

class Lexer():

    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.forward()

    def forward(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_space(self):
        while self.current_char.isspace() and self.current_char is not None:
            self.forward()

    def build_num(self):
        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.forward()
        return Token('NUMBER', int(num)) # may need to change NUMBER to search through token array or soemthing?
    
    def build_word(self):
        word = ''
        while self.current_char is not None and not self.current_char.isspace():
            word += self.current_char
            self.forward()
        return Token(word.upper(), word.lower())
    
    def get_val(self, key):
        for token in token_types:
            if token[0] == key:
                return token[1]
    
    def build_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_space()
            elif self.current_char.isdigit():
                tokens.append(self.build_num())
            elif self.current_char.isalpha():
                tokens.append(self.build_word())
            elif self.current_char == self.get_val('ASSIGN'):
                tokens.append(Token('ASSIGN', self.get_val('ASSIGN')))
                self.forward()
            elif self.current_char == self.get_val('UNION'):
                tokens.append(Token('UNION', self.get_val('UNION')))
                self.forward()
            else:
                break

        tokens.append(Token('END', self.get_val('END')))
        return tokens
    

if __name__ == '__main__': # Test usage
    text_input = 'video = image + audio'
    lex = Lexer(text_input)
    token_stream = lex.build_tokens()
    for token in token_stream:
        print(token.toString())