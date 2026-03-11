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
    ('QUOTES', '"'),
    ('COMMA', ','),
    ('COLON', ':'),
    ('PERIOD', '.')
    #('NUMBER', '0') # need to figure this one out - example: timestamps, effect values
    #('LITERAL', 'x'), # need to figure this one out - example: variable filepaths (user defined)
    #('IDENTIFIER', 'x'), # need to figure this one out - example: video variable name (user defined)
    #('END', '') # end of text
)

media_types = ['video', 'audio', 'image']
effects = ['blur', 'saturation', 'chroma']
timestamp_symbols = [')', ',']

token_map = dict(token_types)
symbols = list(token_map.values())

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
        while self.current_char is not None and self.current_char.isspace():
            self.forward()

    def build_num(self):
        num = ''
        while self.current_char is not None and self.current_char not in timestamp_symbols:
            num += self.current_char
            self.forward()
        
        if ':' in num:
            key = 'TIMESTAMP'
        else:
            key = 'NUMBER'

        return Token(key, num) # may need to change NUMBER to search through token array or soemthing?
    
    def build_word(self):
        word = ''
        while self.current_char is not None and not self.current_char.isspace() and self.current_char not in symbols:
            word += self.current_char
            self.forward()
        
        if word in media_types:
            key = 'TYPE'
        elif word in effects:
            key = 'EFFECT'
        else:
            key = 'IDENTIFIER'

        return Token(key, word)
    
    def build_definition(self):
        definition = ''
        while self.current_char is not None and not self.current_char.isspace():
            definition += self.current_char
            self.forward()

        return Token('DEFINITION', definition)
    
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
            elif self.current_char == self.get_val('FUNC_COMP'):
                tokens.append(Token('FUNC_COMP', self.get_val('FUNC_COMP')))
                self.forward()
            elif self.current_char == self.get_val('LPAREN'):
                tokens.append(Token('LPAREN', self.get_val('LPAREN')))
                self.forward()
            elif self.current_char == self.get_val('RPAREN'):
                tokens.append(Token('RPAREN', self.get_val('RPAREN')))
                self.forward()
            elif self.current_char == self.get_val('QUOTES'):
                tokens.append(self.build_definition())
                self.forward()
            elif self.current_char == self.get_val('COMMA'):
                tokens.append(Token('COMMA', self.get_val('COMMA')))
                self.forward()
            elif self.current_char == self.get_val('COLON'):
                tokens.append(Token('COLON', self.get_val('COLON')))
                self.forward()
            elif self.current_char == self.get_val('PERIOD'):
                tokens.append(Token('PERIOD', self.get_val('PERIOD')))
                self.forward()
            else:
                raise Exception(f"Illegal input: {self.current_char}")

        tokens.append(Token('END', self.get_val('END')))
        return tokens

if __name__ == '__main__': # Test usage
    text_input = 'audio a_1 = "epic_song.mp3" (0,1:45.42)'
    lex = Lexer(text_input)
    token_stream = lex.build_tokens()
    for token in token_stream:
        print(token.toString())