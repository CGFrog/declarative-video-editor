from src.compiler.StateVariable import StateVariable

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

class VideoVariable(StateVariable):
    def __init__(self, effects=None, clips=None, type=""):
        super().__init__(type)
        self.effects: list[Effect] = effects if effects is not None else []
        self.clips: list[Clip] = clips if clips is not None else []

    def __eq__(self, other)-> bool:
        if isinstance(other, VideoVariable):
            return self.type == other.type and self.clips == other.clips and self.effects == other.effects
        return False
    
    def __repr__(self)->str:
        return f"""
        Type: {self.type} \n
        Clips: {self.clips}\n
        Effects: {self.effects}

        """
    
