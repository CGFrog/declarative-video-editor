from src.compiler.Effect import Effect

class Clip:
    def __init__(self, path : str, duration : list[str]):
        self.path: str = path
        self.duration: list[str] = duration

class StateVariable:
        def __init__(self):
            self.effects: list[Effect] = []
            self.clips: list[Clip] = []
            self.duration: list[str] = [] 

        def add_effect(self, effect):
            self.effects.append(effect)
        
        def set_duration(self, timestamp: str):
            self.duration.append(timestamp)