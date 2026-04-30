from src.compiler.lexer.Token import TokenLabel as TL
from src.compiler.lexer.Token import Token

# --- Single character symbols used in our language --- #
symbols = {
    '=': TL.ASSIGN,
    '+': TL.UNION,
    '(': TL.LPAREN,
    ')': TL.RPAREN,
    '[': TL.LBRACK,
    ']': TL.RBRACK,
    ',': TL.COMMA,
    '.': TL.PERIOD,
    ':': TL.COLON
}

# --- Types, effects, and keywords used in our language --- #
labels = {
    'video': TL.MEDIA,
    'audio': TL.MEDIA,
    'image': TL.MEDIA,
    'blur': TL.EFFECT,
    'saturation': TL.EFFECT,
    'chroma': TL.EFFECT,
    'transform': TL.EFFECT,
    'scale': TL.EFFECT,
    'noise_filter': TL.EFFECT,
    'volume': TL.EFFECT,
    'speed': TL.EFFECT,

    'timeline': TL.TIMELINE,
    'after': TL.AFTER,
    'render': TL.RENDER,
    'func': TL.FUNC,

    # Primitive Variables
    'str': TL.STR,
    'num': TL.NUM,
    'caption': TL.CAPTION
}

# Import token class
from src.compiler.lexer.Token import Token

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
        start = self.pos
        num = ''
        while self.current_char != None and (self.current_char.isdigit() or self.current_char == '-' or self.current_char == '.'):
            num += self.current_char
            self.__forward()
        end = self.pos
        return Token(TL.NUMBER, num, start,end )
    
    def __build_word(self):
        start =self.pos
        word = ''
        while self.current_char is not None and not self.current_char.isspace() and self.current_char not in symbols:
            word += self.current_char
            self.__forward()

        end = self.pos
        token_key = None

        if word in labels:
            token_key = labels[word]

        if word == 's': token_key = TL.START_OF_VID
        if word == 'e': token_key = TL.END_OF_VID
        if token_key is None: token_key = TL.IDENTIFIER

        return Token(token_key, word,start, end)
    
    def __build_definition(self):
        definition: str = ''
        start = self.pos
        self.__forward() # Assumes we enter build definition on some indicator token like "
        while self.current_char is not None and self.current_char != '"':
            definition += self.current_char
            self.__forward()
        self.__forward()
        end = self.pos
        return Token(TL.DEFINITION, definition,start, end)
    
    def build_tokens(self, text : str) -> list[Token]:
        tokens = []
        self.text = text
        self.pos = -1
        self.current_char = None
        self.__forward()

        while self.current_char is not None and self.current_char != '%':
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
                start = self.pos
                self.__forward()
                if self.current_char == '>':
                    tokens.append(Token(TL.FUNC_COMP, '|>', start, self.pos))
                    self.__forward()
                else:
                    raise Exception(f"Illegal input: {self.current_char}")
            elif self.current_char in symbols: # Check for all other characters in the langauge
                key = symbols[self.current_char]
                tokens.append(Token(key, self.current_char,self.pos,self.pos))
                self.__forward()
            else:
                raise Exception(f"Illegal input: {self.current_char}")

        tokens.append(Token(TL.END_OF_LINE, '',self.pos,self.pos)) # Indicates end of line
        return tokens

# --- Test Usage --- #
if __name__ == '__main__':
    text_input = 'render "file.mp4" [1920,1080]'
    lex = Lexer()
    # token_stream = lex.build_tokens(text=text_input)
    token_stream = lex.build_tokens(text='render "file.mp4" [1920,1080]')
    for token in token_stream:
        print(token.toString())