from enum import Enum


class Label(Enum):
    TYPE = 1
    EFFECT = 2
    KEYWORD = 3
    ASSIGN = 4
    UNION = 5
    LPAREN = 6
    RPAREN = 7
    LBRACK = 8
    RBRACK = 9
    COMMA = 10
    PERIOD = 11
    COLON = 12


# --- Single character symbols used in our language --- #
symbols = {
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

# --- Types, effects, and keywords used in our language --- #
labels = {
    'video': 'TYPE',
    'audio': 'TYPE',
    'image': 'TYPE',
    'blur': 'EFFECT',
    'saturation': 'EFFECT',
    'chroma': 'EFFECT',
    'transform': 'EFFECT',
    'scale': 'EFFECT',
    'noise_filter': 'EFFECT',
    'volume': 'EFFECT',
    'speed': 'EFFECT',
    'timeline': 'KEYWORD',
    'after': 'KEYWORD',
    'render': 'KEYWORD'
}

# Import token class
from Token import Token

class Lexer():

    def __init__(self):
        self.pos = -1
        self.current_char : str | None = None
        self.text: str = ""

    def __forward(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def __skip_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.__forward()

    def __build_num(self):
        num = ''
        assert(self.current_char is not None)
        while self.current_char.isdigit() or self.current_char == '-' or self.current_char == '.':
            num += self.current_char
            self.__forward()

        return Token('NUMBER', num)
    
    def __build_word(self):
        word = ''
        while self.current_char is not None and not self.current_char.isspace() and self.current_char not in symbols:
            word += self.current_char
            self.__forward()

        token_key = None

        if word in labels:
            token_key = labels[word]

        if word == 's': token_key = 'START_OF_VID'
        if word == 'e': token_key = 'END_OF_VID'
        if token_key is None: token_key = 'IDENTIFIER'

        return Token(token_key, word)
    
    def __build_definition(self):
        definition = ''
        while self.current_char is not None and not self.current_char.isspace():
            definition += self.current_char
            self.__forward()

        return Token('DEFINITION', definition)
    
    def build_tokens(self, text : str) -> list[Token]:
        tokens = []
        self.text = text
        self.__forward()

        while self.current_char is not None:
            if self.current_char.isspace(): # Check for space
                self.__skip_space()
            elif self.current_char.isdigit() or self.current_char == '-': # Check for numbers (supports negatives)
                tokens.append(self.__build_num())
            elif self.current_char.isalpha(): # Check for words (types, effects, keywords, identifiers)
                tokens.append(self.__build_word())
            elif self.current_char == '"': # Check for filepath definitions
                tokens.append(self.__build_definition())
                self.__forward()
            elif self.current_char == '|': # Check for function composition |>
                self.__forward()
                if self.current_char == '>':
                    tokens.append(Token('FUNC_COMP', '|>'))
                    self.__forward()
                else:
                    raise Exception(f"Illegal input: {self.current_char}")
            elif self.current_char in symbols: # Check for all other characters in the langauge
                key = symbols[self.current_char]
                tokens.append(Token(key, self.current_char))
                self.__forward()
            else:
                raise Exception(f"Illegal input: {self.current_char}")

        tokens.append(Token('END_OF_LINE', '')) # Indicates end of line
        return tokens

# --- Test Usage --- #
if __name__ == '__main__':
    text_input = 'video intro = "intro.mp4" (1:45.33,e) |> saturation(3) |> speed(1.5)'
    lex = Lexer()
    token_stream = lex.build_tokens(text=text_input)
    for token in token_stream:
        print(token.toString())