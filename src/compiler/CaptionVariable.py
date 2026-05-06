from compiler.StateVariable import StateVariable


class CaptionVariable(StateVariable):
    def __init__(self, identifier, text, duration):
        super().__init__("text")
        self.identifier = identifier
        self.text = text
        self.duration = duration

    def __eq__(self, other):
        if isinstance(other, CaptionVariable):
            return self.identifier == other.identifier and self.text == other.text and self.duration == other.duration