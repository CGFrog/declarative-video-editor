from src.compiler.lexer.Token import Token
from src.compiler.lexer.Token import TokenLabel as TL
from src.compiler.parser.ParsingUtils import first_of_token, extract_function_parameters
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.parser.RenderSettings import RenderSettings
class TimelineParser:
    def __init__(self):
        self.timeline_elements: list[TimelineElement] = []
        self.render_settings: RenderSettings | None = None
        
    def parse_source(self, lines_of_tokens: list[list[Token]]):
        """
        Takes in a list of tokens and returns a timeline structure of the videos.
        """
        for tokens in lines_of_tokens:
            if len(tokens) == 0:
                continue        
            token: TL = tokens[0].key
            match token:
                case TL.IDENTIFIER:
                    self.timeline_elements.append(self.__parse_media_line(tokens))
                case TL.RENDER:
                    self.render_settings= self.__parse_render_line(tokens)

    def __parse_render_line(self, tokens : list[Token]):
        index: int = 0       
        params : tuple[str, str] | None = None 
        export_path: str | None = None 
        while index < len(tokens):
            match tokens[index].key:
                case TL.DEFINITION:
                    export_path = tokens[index].value
                case TL.LBRACK:
                    rbrack: int = first_of_token(tokens[index + 1::], TL.RBRACK) + index
                    render_params = extract_function_parameters(tokens[index + 1:rbrack+1:])
                    params = tuple(render_params)
            index += 1
        if export_path == None or params == None:
            raise Exception("Invalid render settings specified.")
        return RenderSettings(export_path, params)

    def __parse_media_line(self, tokens: list[Token]):
        z : str | None = ""
        start_time: str | None = ""
        index : int = 0
        after: bool = False 
        identifier : str | None = tokens[0].value
        while index < len(tokens):
            token: Token = tokens[index]
            match token.key:
                case TL.NUMBER:
                    if after:
                        z = token.value
                    else:
                        if start_time=="":
                            start_time = token.value
                        else:
                            z= token.value
                case TL.AFTER:
                    after = True
                    try:
                        start_time = tokens[index + 1].value
                    except:
                        raise Exception("No valid identifier specified after 'after'")
                    pass
            index += 1
        return TimelineElement(identifier,start_time, z )
        
