from collections import defaultdict
import json
import subprocess
from typing import Dict, List
from src.compiler.parser.Parser import Parser
from src.compiler.StateVariable import Clip, StateVariable
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.FFMpegBuilder import FFMpegBuilder

class ResolvedClip:
    def __init__(self, path, src_start, src_end, timeline_start, z):
        self.path = path
        self.src_start = src_start
        self.src_end = src_end
        self.timeline_start = timeline_start
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
        render_settings = self.parser.render_settings

        clips = self.__generate_clips()
        layers = self.__build_layers(clips)
        ffmpeg_builder = FFMpegBuilder()
        
        filter_complex = ffmpeg_builder.build_filter_graph(layers, int(render_settings.x), int(render_settings.y) )
        inputs = ffmpeg_builder.build_inputs()

        output_path = self.parser.render_settings.export_path
        final_v = ffmpeg_builder.final_video_label

        return (
            f"ffmpeg {inputs} "
            f"-filter_complex \"{filter_complex}\" "
            f"-map \"[{final_v}]\" -map \"[a]\" "
            f"\"{output_path}\""
        )

    def __generate_clips(self):
        result: list[ResolvedClip] = []
        for timeline_element in self.timeline:
            base_start = self.__resolve_start_time(timeline_element.identifier)
            z: int = int(timeline_element.z)
            state: StateVariable = self.state[timeline_element.identifier]
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
    
    def __build_layers(self, clips:list[ResolvedClip]):
        layers = defaultdict(list) # This is a neat trick, initializes all elements in the dict to list.
        for clip in clips:
            layers[clip.z].append(clip)
        for z in layers:
            layers[z].sort(key=lambda c: c.timeline_start)
        return layers

def main():
    source_code = """
    video intro = "C:\\Users\\ianco\\Downloads\\DVEL\\full_video.mp4" (0,5)
    video intro2 = "C:\\Users\\ianco\\Downloads\\DVEL\\full_video.mp4" (0,5)
    timeline
    intro 5 1
    render "output.mp4" [1920,1080]
    """

    compiler = Compiler()
    command = compiler.compile(source_code)

    print("Generated FFmpeg command:\n")
    print(command)

    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    main()
