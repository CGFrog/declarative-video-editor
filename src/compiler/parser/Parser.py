from re import L

from networkx import line_graph
from torch import empty

from lexer.Lexer import Lexer
from lexer.Token import Token
from lexer.Token import TokenLabel as TL

class Parser():
    def __init__(self, lexer : Lexer):
        self.lexer : Lexer = lexer
        self.state: dict = {}
        self.timeline : dict = {}

    def parse_source(self, source_code : str):
        lines_of_code : list[str] = source_code.splitlines()
        line_number = 1
        for line in lines_of_code:
            tokens = self.lexer.build_tokens(line)
            if len(tokens) == 0:
                continue
            
            token = tokens[0].key
            # There are only four things a line might do, create media, signal start the timeline, add media to timeline, or render.
            match token:  
                case TL.END_OF_LINE:
                    # White space, just ignore.
                    break
                case TL.MEDIA:
                    if tokens[1].key != TL.IDENTIFIER: 
                        raise Exception(f"Invalid identifier after type declaration.")
                    self.state[tokens[1].value] =  self.__parse_media(tokens, line_number)
                    break
                case TL.TIMELINE:
                    # Timeline is semantic sugar at this point, we may be able to just get rid of it.
                    break
                
                case TL.IDENTIFIER:
                    self.timeline[tokens[1].value] = self.__parse_timeline_instance(tokens, line_number)
                    break

                case TL.RENDER:
                    # signal to compiler we are ready to compile the video.
                    break

    def __parse_media(self, tokens : list[Token], line_number: int):
        token = tokens[0]
        current_operator : TL | None = None
        while token.key != TL.END_OF_LINE:
            match token.key:
                case TL.UNION:
                    current_operator = TL.UNION
                    break
                case TL.DEFINITION:
                    current_operator = TL.DEFINITION
                    break
                case TL.LPAREN:
                    
                    break
                case TL.LBRACK:
                    break
                case TL.FUNC_COMP:
                    current_operator = TL.FUNC_COMP
                    break
                case _:
                    raise Exception(f"Invalid syntax on line {line_number}")

    def __parse_timeline_instance(self, tokens : list[Token],line_number: int):
        pass

    def __parse_parenthesis(self, tokens : list[Token], current_operator : TL):
        pass

    def __parse_brackets(self, tokens : : list[Token], current_operator : TL):
        pass