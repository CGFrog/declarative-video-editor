from src.compiler.lexer.Lexer import Lexer
from src.compiler.parser.DeclarationParser import DeclarationParser
from src.compiler.lexer.Token import Token
from src.compiler.lexer.Token import TokenLabel as TL
class Parser():
    def __init__(self, lexer : Lexer):
        self.lexer : Lexer = lexer
        self.state: dict = {} # Holds all media variables, i.e. videos, audio, and images, as well as their attributes such as effects applied and durations.
        self.timeline : dict = {} # Tells the compiler how to organize our video.
        self.line_number : int = 1

    def parse_source(self, source_code : str):
        lines_of_code : list[str] = source_code.splitlines()
        declaration_tokens: list[list[Token]] = []
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
        # timeline_parser = TimelineParser()

        self.state = declaration_parser.parse_source(declaration_tokens)
        # generate state step here
        # generate timeline step here

def main():
    source_code =   "video intro = \"intro.mp4\" (0,e) |> saturation(3) |> speed(1.5)"\
                    "audio music = \"music.mp3\" (0,e) |> volume(2) |> noise_filter(-60)"\
                    "video game_footage = \"game_footage.mp4\" (0,30) + (35,49)"\
                    "video webcam_footage = \"webcam_footage.mp4\" (0,30) + (35,49) |> transform(1000,320) |> scale(0.2,0.2)"\
                    ""\
                    ""\
                    "timeline"\
                    "intro 0 1"\
                    "game_footage after intro 1"\
                    "music 0 1"\
                    "webcam_footage after intro 2"\
                    ""\
                    "render \"lets_play.mp4\" [1920,1080]"
    lexer = Lexer()
    parser = Parser(lexer)
    parser.parse_source(source_code)
    print(parser)


if __name__ == '__main__':
    main()