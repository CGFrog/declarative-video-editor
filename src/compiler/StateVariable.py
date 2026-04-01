from Effect import Effect

class StateVariable:
        def __init__(self, clip: tuple):
            self.effects: list[Effect] = []
            self.clips = clip 
            self.duration: list[str] | None = None 

        def add_effect(self, effect):
            self.effects.append(effect)
        
        def set_duration(self, timestamp: str):
            self.duration.append(timestamp)