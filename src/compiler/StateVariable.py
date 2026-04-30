from src.compiler.Effect import Effect

class StateVariable:
    def __init__(self, type=""):
        self.type: str = type

    def __eq__(self, other)-> bool:
        if isinstance(other, StateVariable):
            return self.type == other.type
        return False
    
    def __repr__(self)->str:
        return f"""
        Type: {self.type} \n
        """
