# --- Single character symbols used in our language --- #
token_symbols = {
    '=': 'ASSIGN',
    '+': 'UNION',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '[': 'LBRACK',
    ']': 'RBRACK',
    ',': 'COMMA',
    '.': 'PERIOD',
    ':': 'COLON'
}
symbols = list(token_symbols.keys())

# --- Types, effects, and keywords used in our language --- #
labels = {
    'TYPE': ['video', 'audio', 'image'],
    'EFFECT': ['blur', 'saturation', 'chroma', 'transform', 'scale', 'noise_filter', 'volume', 'speed'],
    'KEYWORD': ['timeline', 'after', 'render']
}

# --- Token Class --- #
class Token():

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toString(self):
        return f"({self.key}, {self.value})"

# --- Lexer Class --- #
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
        while self.current_char.isdigit() or self.current_char == '-' or self.current_char == '.':
            num += self.current_char
            self.forward()

        return Token('NUMBER', num)
    
    def build_word(self):
        word = ''
        while self.current_char is not None and not self.current_char.isspace() and self.current_char not in symbols:
            word += self.current_char
            self.forward()

        token_key = None

        for key, value in labels.items():
            if word in value:
                token_key = key

        if word == 's': token_key = 'START_OF_VID'
        if word == 'e': token_key = 'END_OF_VID'
        if token_key is None: token_key = 'IDENTIFIER'

        return Token(token_key, word)
    
    def build_definition(self):
        definition = ''
        while self.current_char is not None and not self.current_char.isspace():
            definition += self.current_char
            self.forward()

        return Token('DEFINITION', definition)
    
    def build_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace(): # Check for space
                self.skip_space()
            elif self.current_char.isdigit() or self.current_char == '-': # Check for numbers (supports negatives)
                tokens.append(self.build_num())
            elif self.current_char.isalpha(): # Check for words (types, effects, keywords, identifiers)
                tokens.append(self.build_word())
            elif self.current_char == '"': # Check for filepath definitions
                tokens.append(self.build_definition())
                self.forward()
            elif self.current_char == '|': # Check for function composition |>
                self.forward()
                if self.current_char == '>':
                    tokens.append(Token('FUNC_COMP', '|>'))
                    self.forward()
                else:
                    raise Exception(f"Illegal input: {self.current_char}")
            elif self.current_char in symbols: # Check for all other characters in the langauge
                for key, value in token_symbols.items():
                    if self.current_char == key:
                        tokens.append(Token(value, key))
                        self.forward()
            else:
                raise Exception(f"Illegal input: {self.current_char}")

        tokens.append(Token('END_OF_LINE', '')) # Indicates end of line
        return tokens

# --- Test Usage --- #
if __name__ == '__main__':
    text_input = 'video intro = "intro.mp4" (1:45.33,e) |> saturation(3) |> speed(1.5)'
    lex = Lexer(text_input)
    token_stream = lex.build_tokens()
    for token in token_stream:
        print(token.toString())