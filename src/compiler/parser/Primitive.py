class Primitive:
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Primitive({self.type}, {self.value})"
    
    def __eq__(self, other):
        if not isinstance(other, Primitive):
            return False
        return self.type == other.type and self.value == other.value