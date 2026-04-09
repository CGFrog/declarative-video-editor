import sys
from src.compiler.lexer.Lexer import Lexer
from src.compiler.lexer.Token import Token
from src.compiler.lexer.Token import TokenLabel as TL
test1 = 'video intro = "intro.mp4" (0,e) |> saturation(3) |> speed(1.5)'
expected1 = [
    Token(TL.MEDIA, 'video'),
    Token(TL.IDENTIFIER, 'intro'),
    Token(TL.ASSIGN, '='),
    Token(TL.DEFINITION, "intro.mp4"),
    Token(TL.LPAREN, '('),
    Token(TL.NUMBER, '0'),
    Token(TL.COMMA, ','),
    Token(TL.END_OF_VID, 'e'),
    Token(TL.RPAREN, ')'),
    Token(TL.FUNC_COMP, '|>'),
    Token(TL.EFFECT, 'saturation'),
    Token(TL.LPAREN, '('),
    Token(TL.NUMBER, '3'),
    Token(TL.RPAREN, ')'),
    Token(TL.FUNC_COMP, '|>'),
    Token(TL.EFFECT, 'speed'),
    Token(TL.LPAREN, '('),
    Token(TL.NUMBER, '1.5'),
    Token(TL.RPAREN, ')'),
    Token(TL.END_OF_LINE, '')
]

test2 = 'video webcam_footage = "webcam_footage.mp4" (0,30) + (35,49) |> transform(1000,320) |> scale(0.2,0.2)'
expected2 = [
    Token(TL.MEDIA, 'video'),
    Token(TL.IDENTIFIER, 'webcam_footage'),
    Token(TL.ASSIGN, '='),
    Token(TL.DEFINITION, "webcam_footage.mp4"),
    Token(TL.LPAREN, '('),
    Token(TL.NUMBER, '0'),
    Token(TL.COMMA, ','),
    Token(TL.NUMBER, '30'),
    Token(TL.RPAREN, ')'),
    Token(TL.UNION, '+'),
    Token(TL.LPAREN, '('),
    Token(TL.NUMBER, '35'),
    Token(TL.COMMA, ','),
    Token(TL.NUMBER, '49'),
    Token(TL.RPAREN, ')'),
    Token(TL.FUNC_COMP, '|>'),
    Token(TL.EFFECT, 'transform'),
    Token(TL.LPAREN, '('),
    Token(TL.NUMBER, '1000'),
    Token(TL.COMMA, ','),
    Token(TL.NUMBER, '320'),
    Token(TL.RPAREN, ')'),
    Token(TL.FUNC_COMP, '|>'),
    Token(TL.EFFECT, 'scale'),
    Token(TL.LPAREN, '('),
    Token(TL.NUMBER, '0.2'),
    Token(TL.COMMA, ','),
    Token(TL.NUMBER, '0.2'),
    Token(TL.RPAREN, ')'),
    Token(TL.END_OF_LINE, '')
]

test3 = 'game_footage after intro 1'
expected3 = [
    Token(TL.IDENTIFIER, 'game_footage'),
    Token(TL.AFTER, 'after'),
    Token(TL.IDENTIFIER, 'intro'),
    Token(TL.NUMBER, '1'),
    Token(TL.END_OF_LINE, '')
]

test4 = 'render "lets_play.mp4" [1920,1080]'
expected4 = [
    Token(TL.AFTER, 'render'),
    Token(TL.DEFINITION, "lets_play.mp4"),
    Token(TL.LBRACK, '['),
    Token(TL.NUMBER, '1920'),
    Token(TL.COMMA, ','),
    Token(TL.NUMBER, '1080'),
    Token(TL.RBRACK, ']'),
    Token(TL.END_OF_LINE, '')
]

def get_token_stream(line : str):
    return Lexer().build_tokens(line);
    
def get_test(test_num : int):
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
    test_input, expected_output = get_test(test_num)
    user_output = get_token_stream(test_input)
    assert user_output == expected_output
    print("\nTEST PASSED")