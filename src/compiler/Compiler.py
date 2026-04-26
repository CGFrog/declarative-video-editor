from collections import defaultdict
import json
import subprocess
from typing import Dict, List
from src.compiler.parser.Parser import Parser
from src.compiler.StateVariable import StateVariable
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.FFMpegBuilder import FFMpegBuilder
from src.compiler.ResolvedClip import ResolvedClip
class Compiler:
    """
    The compiler works by concatenating the videos together on each layer, and overlay the layers on top of each other.
    """
    def __init__(self):
        self.parser = Parser()
        self.state: Dict[str, StateVariable] = {}
        self.timeline: List[TimelineElement] = []
        self.input_index: Dict[str, int] = {}
        self.next_index: int = 0
        self.layers = {}
        self.duration_cache: dict[str,float] = {}

    def compile(self, source_code: str)->str:
        self.parser.parse_source(source_code=source_code)
        self.state = self.parser.state
        self.timeline = self.parser.timeline
        
        assert self.parser.render_settings is not None
        render_settings = self.parser.render_settings

        clips = self.__generate_clips()
        layers: dict = self.__build_layers(clips)
        ffmpeg_builder = FFMpegBuilder()
        
        # generates the ffmpeg command
        filter_complex: str = ffmpeg_builder.build_filter_graph(layers, int(render_settings.x), int(render_settings.y) )

        # Handles text elements
        if (self.text_elements):
            filter_parts_extra = self.__handle_text(ffmpeg_builder)
            filter_complex = filter_complex + ";" + ";".join(filter_parts_extra)

        # resolves all of the inputs for the ffmpeg command.
        inputs: str = ffmpeg_builder.build_inputs()

        output_path:str = self.parser.render_settings.export_path
        final_v:str = ffmpeg_builder.final_video_label
        final_a:str = ffmpeg_builder.final_audio_label
        # returns the ffmpeg command as a string to reduce side-effects, that way users can compile and to see errors often without generating a whole video.
        return (
            f"ffmpeg {inputs} "
            f"-filter_complex \"{filter_complex}\" "
            f"-map \"[{final_v}]\" -map \"[{final_a}]\" "
            f"\"{output_path}\""
        )
    
    def __generate_clips(self):
        """
        # Generates new clips that can be more easily used by the ffmpeg builder. Essentially combining timeline clips with their state variable counter parts.
        """
        result: list[ResolvedClip] = []
        self.text_elements = [] # Stores text elements
        for timeline_element in self.timeline:
            base_start = self.__resolve_start_time(timeline_element)
            z: int = int(timeline_element.z)
            state: StateVariable = self.state.get(timeline_element.identifier)
            if type(state).__name__ == 'TextVariable': # If text variable detected, append to text_elements and continue
                self.text_elements.append({
                    "text": state.text,
                    "start": timeline_element.start_time,
                    "duration": state.duration,
                    "z": z
                })
                continue
            cursor = base_start
            for clip in state.clips:
                start = float(clip.duration[0]) if clip.duration[0] else 0
                end = self.__get_media_duration(clip.path) if clip.duration[1] == 'e' else float(clip.duration[1])
                duration = end -start
                if (end < start):
                    raise Exception(f"Clip {clip.path} ({start},{end}) cannot have negative duration.")
                result.append(
                    ResolvedClip(
                        path=clip.path,
                        src_start=start,
                        src_end=end,
                        timeline_start=cursor,
                        z=z,
                        effects=state.effects
                    )
                )
                cursor += duration
        return result

    def __get_media_duration(self, path:str)->float:
        """
        Uses ffprobe to find the duration of a video.
        """
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
    
    def __resolve_start_time(self, element: TimelineElement) -> float:
        """
        x after y, y after z, to find the start time of x we must know the start time of z + duration of z + duration of y, this function calculates that recursively.

        I'd like to be able to re-reference previous variables rather than cyclic dependency errors but with so little time left, this will do.

        If one of you wants to tackle the challege

        We want:

        x after y
        z after y
        x after z

        where the last x is essentially just a copy of the first x with a new start time.
        """
        visited = set()
        def resolve(el: TimelineElement) -> float:
            if id(el) in visited:
                raise Exception(f"Cyclic dependency: {el.identifier}")
            visited.add(id(el))
            try:
                return float(el.start_time)
            except ValueError:
                dep = next(x for x in self.timeline if x.identifier == el.start_time)
                return resolve(dep) + self.__get_state_duration(dep.identifier)

        return resolve(element)

    def __get_state_duration(self, name: str) -> float:
        """
        Finds the duration of a state variable
        """
        state = self.state[name]
        total =0
        for clip in state.clips:
            start:float = float(clip.duration[0]) if clip.duration[0] else 0
            end: float = self.__get_media_duration(clip.path) if clip.duration[1] == "e" else float(clip.duration[1])
            total += end-start
        return total
    
    def __build_layers(self, clips:list[ResolvedClip]):
        """
        Adds video clips to their corresponding layer.
        """
        layers = defaultdict(list) # This is a neat trick, initializes all elements in the dict to list.
        for clip in clips:
            layers[clip.z].append(clip)
        for z in layers:
            layers[z].sort(key=lambda c: c.timeline_start)
        return layers
    
    def __handle_text(self, ffmpeg_builder):
        current_v = ffmpeg_builder.final_video_label
        filter_parts_extra = []

        for text in sorted(self.text_elements, key=lambda t: t['z']):
            current_v = ffmpeg_builder.build_text_overlay(
                text=text["text"],
                timeline_start=text["start"],
                duration=text["duration"],
                z=text["z"],
                filter_parts=filter_parts_extra,
                current_v=current_v
            )

        ffmpeg_builder.final_video_label = current_v

        return filter_parts_extra

def main():
    source_code = """
    video scenery = "C:\\Users\\benbu\\Videos\\IMG_1937.MOV" (0,e)
    video ben = "C:\\Users\\benbu\\Videos\\IMG_1962.MOV" (0,e)
    str t_1 = "Hello World, it is a nice day out!" 2

    timeline

    ben 0 1
    t_1 0 1
    scenery after ben 1
    
    render "output.mp4" [1656,1242]
    """

    compiler = Compiler()
    command = compiler.compile(source_code)
    print(command)
    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    main()
