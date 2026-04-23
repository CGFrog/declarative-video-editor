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
        self.__validate_timeline()

    def __validate_timeline(self):
        """
        Ensures no cyclic dependencies and all identifiers are accounted for.
        """
        seen = set()
        identifiers = {el.identifier for el in self.timeline_elements}
        for element in self.timeline_elements:
            try: # ensure x start time is all good and we have it
                float(element.start_time)
            except ValueError:
                if element.start_time not in identifiers:
                    raise Exception(f"'{element.identifier}' references unknown identifier '{element.start_time}' in 'after'.")
            # ensure an identifier is not user in an after twice, cyclic dependencies are bad, itd be nice to find a better fix for this. 
            if element.identifier in seen:
                raise Exception(f"'{element.identifier}' appears more than once in the timeline. Each variable can only be placed once to avoid ambiguous cyclic dependencies.")
            seen.add(element.identifier)
        identifiers = {el.identifier for el in self.timeline_elements}

    def __parse_render_line(self, tokens : list[Token])-> RenderSettings:
        """
        Parsing for the final render line, this will be modified if we want more than 'render [x,y]'
        """
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
        """
        Parses the x after y or x 0 1 declarations after timeline.
        """
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
                        index += 1
                    except:
                        raise Exception("No valid identifier specified 'after'")
            index += 1
        return TimelineElement(identifier,start_time, z )
        
