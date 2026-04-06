from compiler.lexer.Lexer import Lexer
from compiler.parser.TimelineParser import TimelineParser
from compiler.parser.DeclarationParser import DeclarationParser
from compiler.lexer.Token import Token
from compiler.lexer.Token import TokenLabel as TL

class Parser():
    def __init__(self, lexer : Lexer):
        self.lexer : Lexer = lexer
        self.state: dict = {} # Holds all media variables, i.e. videos, audio, and images, as well as their attributes such as effects applied and durations.
        self.timeline : dict = {} # Tells the compiler how to organize our video.
        self.line_number : int = 1

    def parse_source(self, source_code : str):
        lines_of_code : list[str] = source_code.splitlines()
        declaration_tokens = []
        timeline_tokens = []


        timeline_index = 0
        for line in lines_of_code:
            tokens = self.lexer.build_tokens(line)
            
            if len(tokens) == 0:
                continue

            if tokens[0].key == TL.TIMELINE:
                timeline_index = self.line_number
            elif not timeline_index:
                declaration_tokens.append(tokens)    
            else:
                timeline_tokens.append(tokens)
            self.line_number += 1

        declaration_parser = DeclarationParser()
        timeline_parser = TimelineParser()

        self.state = declaration_parser.parse_source(declaration_tokens)
        # generate state step here
        # generate timeline step here
        