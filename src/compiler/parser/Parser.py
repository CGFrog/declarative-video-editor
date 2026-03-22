from re import L

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
                    self.state[tokens[1].value] =  self.__parse_media(tokens)
                    break
                case TL.TIMELINE:
                    # Timeline is semantic sugar at this point, we may be able to just get rid of it.
                    break
                
                case TL.IDENTIFIER:
                    self.state[tokens[1].value] = self.__parse_timeline_instance(tokens)
                    break

                case TL.RENDER:
                    # signal to compiler we are ready to compile the video.
                    break

    def __parse_media(self, tokens : list[Token]):
        pass
    
    def __parse_timeline_instance(self, tokens : list[Token]):
        pass