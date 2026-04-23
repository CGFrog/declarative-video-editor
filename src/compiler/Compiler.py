import json
import subprocess
import time
from typing import Dict, List
from src.compiler.parser.Parser import Parser
from src.compiler.StateVariable import Clip, StateVariable
from src.compiler.parser.TimelineElement import TimelineElement

class ResolvedClip:
    def __init__(self, path:str, start:float,end:float,z:int):
        self.path = path
        self.start = start
        self.end = end
        self.z = z

class Compiler:
    def __init__(self):
        self.parser = Parser()
        self.state: Dict[str, StateVariable] = {}
        self.timeline: List[TimelineElement] = []
        self.input_index: Dict[str, int] = {}
        self.next_index: int = 0
        self.layers = {}
        self.duration_cache: dict[str,float] = {}

    def compile(self, source_code: str):
        self.parser.parse_source(source_code=source_code)
        self.state = self.parser.state
        self.timeline = self.parser.timeline
        
        assert self.parser.render_settings is not None
        clips = self.__generate_clips()

    def __generate_clips(self):
        result: list[ResolvedClip] = []
        for timeline_element in self.timeline:
            base_start = self.__resolve_start_time(timeline_element.identifier)
            z: int = int(timeline_element.z)
            state: StateVariable = self.state[timeline_element.identifier]
            cursor = base_start
            for clip in state.clips:
                start = float(clip.duration[0])
                end = self.__get_media_duration(clip.path)if end == 'e' else float(clip.duration[1])
                duration = end -start
                if (end-start<= 0):
                    raise Exception(f"Clip {clip.path} ({start},{end}) cannot have negative duration.")
                result.append(
                    ResolvedClip(
                        path=clip.path,
                        start=cursor,
                        end=cursor+duration,
                        z=z
                    )
                )
                cursor += duration
        return result

    def __get_media_duration(self, path:str)->float:
        if path in self.duration_cache:
            return self.duration_cache[path]
        result = subprocess.run(
            [ # useful little ffmpeg trick to get the duration of a video i.e. the end time.
                "ffprobe",
                "-v",
                "error", # gives us an error code to check 
                "-show_entries",
                "format=duration",
                "-of",
                "json",
                path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text =True
        )
        if result.returncode != 0:
            raise Exception(f"Cannot extract duration of clip at path {path}.")
        
        duration = float(json.loads(result.stdout)['format']['duration'])
        self.duration_cache[path] = duration
        return duration
    
    def __resolve_start_time(self, name: str) -> float:
        visited = set()
        def resolve(n: str) -> float:
            if n in visited:
                raise Exception(f"Cyclic dependency: {n}")
            visited.add(n)
            timeline_element = next(x for x in self.timeline if x.identifier==n)
            try:
                return float(timeline_element.start_time)
            except ValueError:
                return resolve(timeline_element.start_time)+self.__get_state_duration(timeline_element.start_time)

        return resolve(name)

    def __get_state_duration(self, name: str) -> float:
        state = self.state[name]
        total =0
        for clip in state.clips:
            start:float = float(clip.duration[0]) if clip.duration[0] else 0
            end: float = self.__get_media_duration(clip.path) if clip.duration[1] == "e" else float(clip.duration[1])
            total += end-start
        return total