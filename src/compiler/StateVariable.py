from src.compiler.Effect import Effect

class Clip:
    def __init__(self, path : str, duration : list[str]):
        self.path: str = path
        self.duration: list[str] = duration

    def __eq__(self, other)-> bool:
        if isinstance(other, Clip):
            return self.path == other.path and self.duration == other.duration
        return False
    
    def __repr__(self) -> str:
        return f"Path: {self.path}\nDuration: {self.duration}"

class StateVariable:
    def __init__(self, effects=[], clips=[], type=""):
        self.effects: list[Effect] = effects
        self.clips: list[Clip] = clips if clips is not None else []
        self.type: str = type

    def __eq__(self, other)-> bool:
        if isinstance(other, StateVariable):
            return self.effects == other.effects and self.clips == other.clips
        return False
    
    def __repr__(self)->str:
        return f"""
        Effects: {[e for e in self.effects]} \n 
        Clips: {[c for c in self.clips]} \n
        Type: {self.type} \n
        """