from enum import Enum

class TokenLabel(Enum):
    MEDIA = 1
    EFFECT = 2
    END_OF_LINE = 3
    ASSIGN = 4
    UNION = 5
    LPAREN = 6
    RPAREN = 7
    LBRACK = 8
    RBRACK = 9
    COMMA = 10
    PERIOD = 11
    COLON = 12
    NUMBER = 13
    DEFINITION = 14
    START_OF_VID = 15
    END_OF_VID = 16
    IDENTIFIER = 17
    FUNC_COMP = 18
    TIMELINE= 19
    RENDER = 20
    AFTER = 21
    STR = 22
    NUM = 23
    FUNC = 24

class Token():
    def __init__(self, key, value, start, end):
        self.key : TokenLabel = key
        self.value : str = value
        self.start : int = start
        self.end : int = end


    def toString(self):
        return f"({self.key}, {self.value})"
    
    def __eq__(self, other)->bool:
        if isinstance(other, Token):
            return self.key == other.key and self.value == other.value
        return False
    