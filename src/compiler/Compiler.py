from typing import Dict, List
from src.compiler.parser.Parser import Parser
from src.compiler.StateVariable import Clip, StateVariable
from src.compiler.parser.TimelineElement import TimelineElement


class Compiler:
    def __init__(self):
        self.parser = Parser()
        self.state: Dict[str, StateVariable] = {}
        self.timeline: List[TimelineElement] = []
        self.input_index: Dict[str, int] = {}
        self.next_index: int = 0
        self.layers = {}
        self.durations: dict[str,float] = {}

    def compile(self, source_code: str):
        self.parser.parse_source(source_code=source_code)
        self.state = self.parser.state
        self.timeline = self.parser.timeline
        
        assert self.parser.render_settings is not None
        
