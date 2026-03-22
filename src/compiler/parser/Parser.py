from lexer.Lexer import Lexer
from lexer.Token import Token

class Parser():
    def __init__(self, lexer : Lexer):
        self.lexer : Lexer = lexer
        self.state: dict = {}

    def parse_source(self, source_code : str):
        lines_of_code : list[str] = source_code.splitlines()
        for line in lines_of_code:
            self.__parse_line_tokens(tokens = self.lexer.build_tokens(text=line))
        
    def __parse_line_tokens(self, tokens : list[Token]):
        # Define order of operations
        # Add variables to state
        pass