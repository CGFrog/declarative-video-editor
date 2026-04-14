from src.compiler.StateVariable import StateVariable
from src.compiler.lexer.Lexer import Lexer
from src.compiler.parser.DeclarationParser import DeclarationParser
from src.compiler.lexer.Token import Token
from src.compiler.lexer.Token import TokenLabel as TL
from src.compiler.StateVariable import StateVariable
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.parser.RenderSettings import RenderSettings


from src.compiler.parser.TimelineParser import TimelineParser
class Parser():
    def __init__(self):
        self.state: dict[str,StateVariable] = {} # Holds all media variables, i.e. videos, audio, and images, as well as their attributes such as effects applied and durations.
        self.timeline : list[TimelineElement] = [] # Tells the compiler how to organize our video.
        self.render_settings: RenderSettings | None = None
        self.line_number : int = 1


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
        self.timeline = timeline_parser.timeline_elements
        self.render_settings = timeline_parser.render_settings
        if self.render_settings == None:
            raise Exception("No render settings specified.")


# Test Case
def main():
    source_code =   """video intro = \"intro.mp4\" (0,e) |> saturation(3) |> speed(1.5)
                    audio music = \"music.mp3\" (0,e) |> volume(2) |> noise_filter(-60)
                    video game_footage = \"game_footage.mp4\" (0,30) + (35,49)
                    video webcam_footage = \"webcam_footage.mp4\" (0,30) + (35,49) |> transform(1000,320) |> scale(0.2,0.2)
                    
                    
                    timeline
                    intro 0 1
                    game_footage after intro 1
                    music 0 1
                    webcam_footage after intro 2
                    
                    render \"lets_play.mp4\" [1920,1080]"""
    parser = Parser()
    parser.parse_source(source_code)
    for name in parser.state.keys():
        print(f"Name: {name}: ")
        print("Clips")
        for clip in parser.state[name].clips:
            print(f"    Path: {clip.path}, Duration: {clip.duration}")
        print("Effects")
        for effect in parser.state[name].effects:
            print(f"    Type: {effect.type}, Params: {effect.param}")
        print("Timeline Parser")
        for t in parser.timeline:
            print(f"    Identifier: {t.identifier}, Start Time: {t.start_time}, z: {t.z}")

if __name__ == '__main__':
    main()