media_types = ['video', 'audio', 'image']
effects = ['blur', 'saturation', 'chroma', 'transform', 'scale', 'noise_filter']
symbols = ['=', '+', '|>', '(', ')', ',', '|']
keywords = ['timeline', 'after']
timestamp_symbols = [')', ',']

class Token():

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toString(self):
        return f"({self.key}, {self.value})"

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

        return Token(key, num)
    
    def build_word(self):
        word = ''
        while self.current_char is not None and not self.current_char.isspace() and self.current_char not in symbols:
            word += self.current_char
            self.forward()
        
        if word in media_types:
            key = 'TYPE'
        elif word in effects:
            key = 'EFFECT'
        elif word in keywords:
            key = 'KEYWORD'
        else:
            key = 'IDENTIFIER'

        return Token(key, word)
    
    def build_definition(self):
        definition = ''
        while self.current_char is not None and not self.current_char.isspace():
            definition += self.current_char
            self.forward()

        return Token('NAME', definition)
    
    def build_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_space()
            elif self.current_char.isdigit():
                tokens.append(self.build_num())
            elif self.current_char.isalpha():
                tokens.append(self.build_word())
            elif self.current_char == '=':
                tokens.append(Token('ASSIGN', '='))
                self.forward()
            elif self.current_char == '+':
                tokens.append(Token('UNION', '+'))
                self.forward()
            elif self.current_char == '|':
                self.forward()
                if self.current_char == '>':
                    tokens.append(Token('FUNC_COMP', '|>'))
                    self.forward()
                else:
                    raise Exception(f"Illegal input: {self.current_char}")
            elif self.current_char == ')':
                tokens.append(Token('LPAREN', '('))
                self.forward()
            elif self.current_char == '(':
                tokens.append(Token('RPAREN', ')'))
                self.forward()
            elif self.current_char == '"':
                tokens.append(self.build_definition())
                self.forward()
            elif self.current_char == ',':
                tokens.append(Token('COMMA', ','))
                self.forward()
            else:
                raise Exception(f"Illegal input: {self.current_char}")

        tokens.append(Token('END', ''))
        return tokens

if __name__ == '__main__': # Test usage
    text_input = 'game_footage after intro 1'
    lex = Lexer(text_input)
    token_stream = lex.build_tokens()
    for token in token_stream:
        print(token.toString())