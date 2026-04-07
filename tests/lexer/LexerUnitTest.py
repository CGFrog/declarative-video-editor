import yaml

from src.compiler.lexer.Lexer import Lexer

lines_to_test = [
    'video intro = "intro.mp4" (0,e) |> saturation(3) |> speed(1.5)',
    'video webcam_footage = "webcam_footage.mp4" (0,30) + (35,49) |> transform(1000,320) |> scale(0.2,0.2)',
    'game_footage after intro 1',
    'render "lets_play.mp4" [1920,1080]'
]

class LexerUnitTest():

    def __init__(self):
        pass

    def run_tests(self, line):
        output_stream = []
        print(f"RUNNING LINE {line}\n")
        lexer = Lexer(line)
        token_stream = lexer.build_tokens();
        for token in token_stream:
            output_stream.append(token.toString())
        
        return output_stream

if __name__ == "__main__":
    ut = LexerUnitTest()

    with open('tests\lexer\LexerTests.yaml', 'r') as file:
        data = yaml.safe_load(file)
        print(data)
        #print(ut.run_tests(lines_to_test[0]))