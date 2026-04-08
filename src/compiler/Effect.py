from enum import Enum

class Effect:
    def __init__(self, effect_type: str, param: list[str]):
        self.type = effect_type
        self.param = param