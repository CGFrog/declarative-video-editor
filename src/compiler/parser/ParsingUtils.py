from src.compiler.lexer.Token import TokenLabel as TL
from src.compiler.lexer.Token import Token

def extract_duration(tokens: list[Token])-> list[str]:
    """
    Takes in a list of tokens and returns the comma separated values as a list of strings
    """
    return "".join(t.value for t in tokens).split(',')
    
def first_of_token(tokens: list[Token], token: TL)-> int:
    """
    Returns the index of the first instance of a token given a list of tokens. If 
    """
    for (i, t) in enumerate(tokens, start=0):
        if t.key == token:
            return i
    return len(tokens)

def extract_function_parameters(tokens: list[Token]) ->list:
    """
    Given a list of tokens of the form:
    (a_1,a_2,...,a_n), returns them as a list of strings.
    """
    params = []
    for token in tokens:
        # If we add effects that take strings as variables, i.e. textboxes of some sort, add an if/match case here.
        if token.key == TL.NUMBER:
            params.append(token.value)
    return params