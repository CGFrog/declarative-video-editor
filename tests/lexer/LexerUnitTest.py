import sys
from src.compiler.lexer.Lexer import Lexer

test1 = 'video intro = "intro.mp4" (0,e) |> saturation(3) |> speed(1.5)'
expected1 = [
    '(TYPE, video)',
    '(IDENTIFIER, intro)',
    '(ASSIGN, =)',
    '(DEFINITION, "intro.mp4")',
    '(LPAREN, ()',
    '(NUMBER, 0)',
    '(COMMA, ,)',
    '(END_OF_VID, e)',
    '(RPAREN, ))',
    '(FUNC_COMP, |>)',
    '(EFFECT, saturation)',
    '(LPAREN, ()',
    '(NUMBER, 3)',
    '(RPAREN, ))',
    '(FUNC_COMP, |>)',
    '(EFFECT, speed)',
    '(LPAREN, ()',
    '(NUMBER, 1.5)',
    '(RPAREN, ))',
    '(END_OF_LINE, )'
]

test2 = 'video webcam_footage = "webcam_footage.mp4" (0,30) + (35,49) |> transform(1000,320) |> scale(0.2,0.2)'
expected2 = [
    '(TYPE, video)',
    '(IDENTIFIER, webcam_footage)',
    '(ASSIGN, =)',
    '(DEFINITION, "webcam_footage.mp4")',
    '(LPAREN, ()',
    '(NUMBER, 0)',
    '(COMMA, ,)',
    '(NUMBER, 30)',
    '(RPAREN, ))',
    '(UNION, +)',
    '(LPAREN, ()',
    '(NUMBER, 35)',
    '(COMMA, ,)',
    '(NUMBER, 49)',
    '(RPAREN, ))',
    '(FUNC_COMP, |>)',
    '(EFFECT, transform)',
    '(LPAREN, ()',
    '(NUMBER, 1000)',
    '(COMMA, ,)',
    '(NUMBER, 320)',
    '(RPAREN, ))',
    '(FUNC_COMP, |>)',
    '(EFFECT, scale)',
    '(LPAREN, ()',
    '(NUMBER, 0.2)',
    '(COMMA, ,)',
    '(NUMBER, 0.2)',
    '(RPAREN, ))',
    '(END_OF_LINE, )'
]

test3 = 'game_footage after intro 1'
expected3 = [
    '(IDENTIFIER, game_footage)',
    '(KEYWORD, after)',
    '(IDENTIFIER, intro)',
    '(NUMBER, 1)',
    '(END_OF_LINE, )'
]

test4 = 'render "lets_play.mp4" [1920,1080]'
expected4 = [
    '(KEYWORD, render)',
    '(DEFINITION, "lets_play.mp4")',
    '(LBRACK, [)',
    '(NUMBER, 1920)',
    '(COMMA, ,)',
    '(NUMBER, 1080)',
    '(RBRACK, ])',
    '(END_OF_LINE, )'
]

class LexerUnitTest():

    def __init__(self):
        pass

    def get_token_stream(self, line : str):
        output_stream = []
        lexer = Lexer(line)
        token_stream = lexer.build_tokens();
        for token in token_stream:
            output_stream.append(token.toString())
        
        return output_stream
    
    def get_test(self, test_num : int):
        match test_num:
            case 1: 
                input_line = test1
                expected_result = expected1
            case 2: 
                input_line = test2
                expected_result = expected2
            case 3: 
                input_line = test3
                expected_result = expected3
            case 4: 
                input_line = test4
                expected_result = expected4
            case _: raise Exception("Unknown Test")

        return input_line, expected_result

if __name__ == "__main__":

    test_num : int = int(sys.argv[1])
    ut = LexerUnitTest()
    test_input, expected_output = ut.get_test(test_num)
    user_output = ut.get_token_stream(test_input)

    print("\nTEST CASE:\n")
    print(f"Input: {test_input}\n")
    for token in user_output:
        print(token)

    assert user_output == expected_output
    print("\nTEST PASSED")