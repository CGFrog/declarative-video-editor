from enum import Enum

class Effect:
        def __init__(self, effect_type: Enum, param: tuple):
            self.type = effect_type
            self.param = param