from src.compiler.StateVariable import StateVariable
from src.compiler.lexer.Lexer import Lexer
from src.compiler.parser.DeclarationParser import DeclarationParser
from src.compiler.lexer.Token import Token
from src.compiler.lexer.Token import TokenLabel as TL
from src.compiler.StateVariable import StateVariable
from src.compiler.VideoVariable import Clip,VideoVariable
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.parser.RenderSettings import RenderSettings
from src.compiler.CaptionVariable import CaptionVariable


from src.compiler.parser.TimelineParser import TimelineParser
class Parser():
    def __init__(self):
        self.state: dict[str,StateVariable | CaptionVariable] = {} # Holds all media variables, i.e. videos, audio, and images, as well as their attributes such as effects applied and durations.
        self.timeline : list[TimelineElement] = [] # Tells the compiler how to organize our video.
        self.render_settings: RenderSettings | None = None
        self.line_number : int = 1
        self.primitives = {}

    def parse_source(self, source_code : str):
        lines_of_code : list[str] = source_code.splitlines()
        lines_of_code = [i.strip() for i in lines_of_code]
        declaration_tokens: list[list[Token]] = []
        timeline_tokens = []
        timeline_index = 0
        for line in lines_of_code:
            lexer : Lexer = Lexer()
            tokens = lexer.build_tokens(line)
            if len(tokens) == 0:
                continue
            if tokens[0].key == TL.TIMELINE:
                timeline_index = self.line_number
            elif timeline_index == 0:
                declaration_tokens.append(tokens)    
            else:
                timeline_tokens.append(tokens)
            self.line_number += 1

        declaration_parser = DeclarationParser()
        timeline_parser = TimelineParser()

        declaration_parser.parse_source(declaration_tokens)
        timeline_parser.parse_source(timeline_tokens)

        self.state = declaration_parser.state
        self.primitives = declaration_parser.primitives
        self.timeline = timeline_parser.timeline_elements
        self.render_settings = timeline_parser.render_settings
        if self.render_settings == None:
            raise Exception("No render settings specified.")