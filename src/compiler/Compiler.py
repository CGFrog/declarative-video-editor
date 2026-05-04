from collections import defaultdict
import json
from plistlib import InvalidFileException
import subprocess
from typing import Dict, List
from src.compiler.parser.RenderSettings import RenderSettings
from src.compiler.parser.Parser import Parser
from src.compiler.StateVariable import StateVariable
from src.compiler.VideoVariable import Clip, VideoVariable
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.FFMpegBuilder import FFMpegBuilder
from src.compiler.ResolvedClip import ResolvedClip
from src.compiler.CaptionVariable import CaptionVariable
class Compiler:
    """
    The compiler works by concatenating the videos together on each layer, and overlay the layers on top of each other.
    """
    def __init__(self):
        self.parser = Parser()
        self.state: Dict[str,StateVariable] = {}
        self.timeline: List[TimelineElement] = []
        self.input_index: Dict[str, int] = {}
        self.next_index: int = 0
        self.layers = {}
        self.duration_cache: dict[str,float] = {}
        self.text_elements = []
        self.clips =[]
        self.duration = None

    def compile(self, source_code: str)->str:
        self.parser.parse_source(source_code=source_code)
        self.state = self.parser.state
        self.timeline = self.parser.timeline

        assert self.parser.render_settings is not None
        render_settings: RenderSettings= self.parser.render_settings

        self.__generate_state_objects()

        if self.clips is None:
            raise Exception("No valid clips.")
        self.layers: dict = self.__build_layers(
            clips=self.clips
        )
        ffmpeg_builder = FFMpegBuilder()
        self.duration = self.__get_total_duration(self.layers)
        # generates the ffmpeg command
        filter_complex: str = ffmpeg_builder.build_filter_graph(
            layers=self.layers,
            width=int(render_settings.x),
            height=int(render_settings.y),
            duration=self.duration
        )

        # Handles text elements
        if (self.text_elements):
            filter_parts_extra = self.__handle_text(
                ffmpeg_builder=ffmpeg_builder
            )
            filter_complex = filter_complex + ";" + ";".join(filter_parts_extra) # Place text filters into ffmpeg graph

        # resolves all of the inputs for the ffmpeg command.
        inputs: str = ffmpeg_builder.build_inputs()

        output_path:str = self.parser.render_settings.export_path
        final_v:str = ffmpeg_builder.final_video_label
        final_a:str = ffmpeg_builder.final_audio_label
        # returns the ffmpeg command as a string to reduce side-effects, that way users can compile and to see errors often without generating a whole video.
        return (
            f"ffmpeg -y {inputs} "
            f"-filter_complex \"{filter_complex}\" "
            f"-map \"[{final_v}]\" -map \"[{final_a}]\" "
            f"\"{output_path}\""
        )
    
    def __generate_state_objects(self): # I hate this function a lot, does so many things at once but itll do for now.
        """
        # Generates new clips, text objects, and audio that can be more easily used by the ffmpeg builder. Essentially combining timeline clips with their state variable counter parts.
        """
        self.text_elements = [] # Stores text elements
        for timeline_element in self.timeline:
            z = 0
            try:
                z: int = int(timeline_element.z)
            except:
                raise Exception(f"z value of {timeline_element.identifier} cannot be converted to an integer.")
            state: StateVariable | None = self.state.get(timeline_element.identifier)
            if state is None:
                raise Exception(f"Cannot access the state of {timeline_element.identifier}")
            if isinstance(state,CaptionVariable): # If text variable detected, append to text_elements and continue
                self.__resolve_text_element(
                    state=state,
                    timeline_element=timeline_element,
                    z=z
                )
            elif isinstance(state,VideoVariable):
                self.__resolve_clips(
                    timeline_element=timeline_element,
                    state=state,
                    z=z
                )
            else:
                #do audio stuff.
                pass

    def __resolve_text_element(self,state,timeline_element,z):
        self.text_elements.append({
            "text": state.text,
            "start": timeline_element.start_time,
            "duration": state.duration,
            "z": z
        })

    def __resolve_clips(self,timeline_element, state : VideoVariable,z:int):
        base_start = self.__resolve_start_time(timeline_element)
        cursor :float = base_start
        for clip in state.clips:
            start = float(clip.duration[0]) if clip.duration[0] else 0
            if state.type == "image":
                if clip.duration[1] == 'e':
                    raise ValueError(
                        f"{timeline_element.identifier}: images require explicit duration, 'e' is not valid."
                    )
                end = float(clip.duration[1])
                full_video_duration = end
            else:
                full_video_duration: float = self.__get_media_duration(path=clip.path)
                end: float = full_video_duration if clip.duration[1] == 'e' else float(clip.duration[1])
                if end > full_video_duration:
                    raise ValueError(f"{timeline_element.identifier} specified duration is longer than the video duration (use 'e' for inclusion of the whole video).")
            duration = end - start
            if (end < start):
                raise Exception(f"Clip {clip.path} ({start},{end}) cannot have negative duration.")
            
            effects = clip.effects if hasattr(clip, 'effects') and clip.effects else state.effects

            for e in effects:
                if e.type == "speed":
                    speed = e.param[0] if len(e.param) > 0 else 1.0
                    duration = duration / float(speed)
            is_audio = False
            if state.type == 'audio': is_audio = True
            self.clips.append(
                ResolvedClip(
                    path=clip.path,
                    src_start=start,
                    src_end=end,
                    timeline_start=cursor,
                    z=z,
                    effects=state.effects,
                    is_audio=is_audio,
                    is_image=state.type == 'image'
                )
            )
            cursor += duration
    
    def __get_total_duration(self, layers) -> float:
        """
        Returns the total duration of the video.
        """
        end_times = []
        
        for clips in layers.values():
            for clip in clips:
                duration = clip.src_end - clip.src_start
                speed = 1.0
                for effect in clip.effects:
                    if effect.type == "speed" and len(effect.param) > 0:
                        speed = float(effect.param[0])
                adjusted_duration = duration / speed
                end_times.append(clip.timeline_start + adjusted_duration)
        return max(end_times)



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
            raise InvalidFileException(f"Cannot extract duration of clip at path {path}.")
        
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
        if isinstance(state, CaptionVariable):
            return float(state.duration)

        if isinstance(state, VideoVariable): # this may be similar for audio might be interchangeable
            total = 0
            for clip in state.clips:
                start:float = float(clip.duration[0]) if clip.duration[0] else 0
                if state.type == 'image':
                    end = float(clip.duration[1])
                else:
                    end: float = self.__get_media_duration(clip.path) if clip.duration[1] == "e" else float(clip.duration[1])
                adjusted = end - start

                for effect in state.effects:
                    if effect.type == "speed":
                        speed = effect.param[0] if len(effect.param) > 0 else 1.0
                        adjusted = adjusted / float(speed)
                total += adjusted
            return total
        # you will need to add an instance check for audio here probably.
        else:
            raise Exception("Unknown class type of state.")


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
        """
        If a text element is detected, create text overlay ffmpeg command, add to filter_parts.
        """
        current_v = ffmpeg_builder.final_video_label # Pointer to current end of the video chain
        filter_parts_extra = []

        for text in sorted(self.text_elements, key=lambda t: t['z']): # Sort by z (layer), lower z draws first
            current_v = ffmpeg_builder.build_text_overlay(
                text=text["text"],
                timeline_start=text["start"],
                duration=text["duration"],
                filter_parts=filter_parts_extra,
                current_v=current_v
            )

        ffmpeg_builder.final_video_label = current_v # current_v holds label of text overlay

        return filter_parts_extra