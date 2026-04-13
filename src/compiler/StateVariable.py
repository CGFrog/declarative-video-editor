from src.compiler.Effect import Effect

class Clip:
    def __init__(self, path : str, duration : list[str]):
        self.path: str = path
        self.duration: list[str] = duration

    def __eq__(self, other)-> bool:
        if isinstance(other, Clip):
            return self.path == other.path and self.duration == other.duration
        return False

class StateVariable:
    def __init__(self):
        self.effects: list[Effect] = []
        self.clips: list[Clip] = []

    def __eq__(self, other)-> bool:
        if isinstance(other, StateVariable):
            return self.effects == other.effects and self.clips == other.clips
        return False