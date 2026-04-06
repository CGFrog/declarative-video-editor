from enum import Enum




class Effect:
        def __init__(self, effect_type: str, param: list[str]):
            # todo switch to enum
            self.type = effect_type
            self.param = param