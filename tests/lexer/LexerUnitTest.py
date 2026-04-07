import yaml
from src.compiler.lexer.Lexer import Lexer

class LexerUnitTest():

    def __init__(self):
        pass

    def run_test(self, line):
        output_stream = []
        lexer = Lexer(line)
        token_stream = lexer.build_tokens();
        for token in token_stream:
            output_stream.append(token.toString())
        
        return output_stream

if __name__ == "__main__":
    ut = LexerUnitTest()

    with open('tests/lexer/LexerTests.yml', 'r') as file:
        data = yaml.safe_load(file)
        last_test = next(reversed(data))
        last_test_num = int("".join(filter(str.isdigit, last_test)))

    for test in range(last_test_num):
        expected_tokens = []
        output_tokens = ut.run_test(data[f'test{test+1}'])
        for token in data[f'expected{test+1}']:
            expected_tokens.append(token)

        assert output_tokens == expected_tokens
        print(f"Test Case {test+1}: PASS")