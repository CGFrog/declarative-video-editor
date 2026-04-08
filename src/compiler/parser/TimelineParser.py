from src.compiler.StateVariable import StateVariable
from src.compiler.lexer.Token import Token
from src.compiler.lexer.Token import TokenLabel as TL
from src.media.DMedia import DMedia

class TimelineElement:
    def __init__(self, start_time, media : DMedia):
        self.start_time = start_time
        self.media = media

class RenderSettings:
    def __init__(self, resolution: tuple[int,int]):
        self.x: int = resolution[0]
        self.y: int = resolution[1]

class TimelineParser:
    def __init__(self):
        self.layer: list[list[TimelineElement]] = []
        self.render_settings: RenderSettings | None = None
        
    def parse_source(self, lines_of_tokens: list[list[Token]], medias : dict[str, DMedia]):
        """
        Takes in a list of tokens and returns a timeline structure of the videos.
        """
        for tokens in lines_of_tokens:
            if len(tokens) == 0:
                continue        
            token: TL = tokens[0].key
            match token:
                case TL.MEDIA:
                    self.__parse_media_line(tokens)

                case TL.RENDER:
                    self.__parse_render_line(tokens)

    def __parse_render_line(self, tokens : list[Token]):
        pass

    def __parse_media_line(self, tokens: list[Token]):
        pass
