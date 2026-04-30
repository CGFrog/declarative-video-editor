from enum import Enum

class Effect:
    def __init__(self, effect_type: str, param: list[str]):
        self.type = effect_type
        self.param = param

    def __eq__(self, other)-> bool:
        if isinstance(other, Effect):
            return self.type == other.type and self.param == other.param
        return False
    
    def __repr__(self)->str:
        return f"Type: {self.type}\nParams: {self.param}"