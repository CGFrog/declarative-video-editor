from uuid import uuid4
from typing import Dict, List, Tuple
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

    def compile(self, source_code: str) -> str:
        self.parser.parse_source(source_code)
        self.state = self.parser.state
        self.timeline = self.parser.timeline
        ordered_clips = self.__resolve_timeline()
        filter_parts: List[str] = []
        stream_nodes: List[Tuple[str, str]] = []

        for clip in ordered_clips:
            video_line, audio_line, labels = self.__build_clip_filters(clip)
            filter_parts.append(video_line)
            filter_parts.append(audio_line)
            stream_nodes.append(labels)

        concat_line = self.__build_concat(stream_nodes)
        filter_parts.append(concat_line)

        filter_complex = ";\n".join(filter_parts)
        inputs = self.__build_inputs()
        
        output_path = ''
        if self.parser.render_settings is not None:
            output_path = self.parser.render_settings.export_path

        if output_path == '':
            raise Exception("No output path specified.")
        
        command = (
            f"ffmpeg {inputs} "
            f"-filter_complex \"{filter_complex}\" "
            f"-map \"[v]\" -map \"[a]\" "
            f"\"{output_path}\""
        )
        return command

    def __get_or_create_input_index(self, path: str) -> int:
        """
        Saves the ffmpeg input index of a given clip.
        """
        index: int | None = self.input_index.get(path)
        if index is not None:
            return index
        index = self.next_index
        self.input_index[path] = index
        self.next_index += 1

        return index

    def __build_inputs(self) -> str:
        items = sorted(self.input_index.items(), key=lambda x: x[1]) # cheeky little lambda to sort by index.
        return " ".join([f'-i "{path}"' for path, _ in items])

    def __build_clip_filters(self, clip: Clip) -> Tuple[str, str, Tuple[str, str]]:
        index = self.__get_or_create_input_index(clip.path)
        start, end = clip.duration

        uid = uuid4().hex[:6]
        video_label = f"v{index}_{uid}"
        audio_label = f"a{index}_{uid}"

        video = f"[{index}:v]trim=start={start}"
        if end != "e":
            video += f":end={end}"
        video += f",setpts=PTS-STARTPTS[{video_label}]"

        audio = f"[{index}:a]atrim=start={start}"
        if end != "e":
            audio += f":end={end}"
        audio += f",asetpts=PTS-STARTPTS[{audio_label}]"

        return video, audio, (video_label, audio_label)


    def __resolve_timeline(self) -> List[Clip]:
        timeline_map = {t.identifier: t for t in self.timeline}

        resolved: List[Tuple[float, int, Clip]] = []

        for t in self.timeline:
            start_time = self.__resolve_start_time(t.identifier, timeline_map)
            z_index = int(t.z)

            state_var = self.state[t.identifier]

            for clip in state_var.clips:
                resolved.append((start_time, z_index, clip))

        resolved.sort(key=lambda x: (x[0], x[1]))

        return [clip for _, _, clip in resolved]

    def __resolve_start_time(self, name: str, timeline_map: Dict[str, TimelineElement]) -> float:
        """
        Orders the timeline elements by earliest 
        """    
        # we love DAGs!
        visited = set()
        def resolve(current: str) -> float:
            if current in visited:
                # x after y, y after x throws this error.
                raise Exception(f"Cyclic timeline reference involving '{current}'")
            visited.add(current)
            t = timeline_map[current]
            val = t.start_time
            try:
                return float(val)
            except ValueError:
                pass
            if val not in timeline_map:
                raise Exception(f"Unknown reference to \"{val}\" in timeline.")

            return resolve(val)
        return resolve(name)
    
    def __build_concat(self, stream_nodes: List[Tuple[str, str]]) -> str:
        parts = []
        for v, a in stream_nodes:
            parts.append(f"[{v}][{a}]")

        concat_inputs = "".join(parts)
        n = len(stream_nodes)
        return f"{concat_inputs}concat=n={n}:v=1:a=1[v][a]"

def main():
    source_code = """video intro = \"C:\\Users\\ianco\\Downloads\\DVEL\\full_video.mp4\" (0,5) + (7,10) |> saturation(3) |> speed(1.5)                
                timeline
                intro 0 1
                render \"lets_play.mp4\" [1920,1080]"""
    compiler = Compiler()
    compiler.compile(source_code=source_code)

if __name__ == "__main__":
    main()