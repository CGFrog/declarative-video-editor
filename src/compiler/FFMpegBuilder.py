from uuid import uuid4
from src.compiler.Effect import Effect
from src.compiler.ResolvedClip import ResolvedClip

class FFMpegBuilder:
    def __init__(self):
        self.input_index: dict[str, int] = {}
        self.next_index: int = 0
        self.final_video_label: str = ""
        self.final_audio_label: str = ""

    def __get_or_create_input_index(self, path: str) -> int:
        """
        Every ffmpeg video in our commands need a unique index to reference them buy. This generates that index or finds the applicable index so we dont have to reload any files.
        """
        if path not in self.input_index:
            self.input_index[path] = self.next_index
            self.next_index += 1
        return self.input_index[path]

    def build_inputs(self) -> str:
        """
        Generates the input line for the ffmpeg command that gets all of our medias.
        """
        sorted_inputs = sorted(self.input_index.items(), key=lambda x: x[1])
        return " ".join(f'-i "{path}"' for path, _ in sorted_inputs)

    def build_filter_graph(self, layers, width: int, height: int) -> str:
        """
        A filter in ffmpeg is a function applied to a media, we are essentially creating a DAG of video and audio with this function.
        """
        filter_parts = []
        layer_outputs = []
        duration = self.__get_total_duration(layers)

        # just add a black video in the background in case any empty gaps, if we wanted to be fancy we could let the user specify what this video is
        black = self.__build_black_base(width, height, duration, filter_parts)

        for z in sorted(layers.keys()):
            v_out, a_out = self.__build_layer(
                clips=layers[z], 
                filter_parts=filter_parts,
                width=width, 
                height=height
            )
            layer_outputs.append((z, v_out, a_out))

        # takes all the layer and computes the final video syntax.
        self.final_video_label = self.__build_overlay_chain(black, layer_outputs, filter_parts)
        self.__build_audio_mix(layer_outputs, filter_parts)

        return ";".join(filter_parts)

    def __get_total_duration(self, layers) -> float:
        """
        Returns the total duration of the video.
        """
        end_times = []
        
        for clips in layers.values():
            for clip in clips:
                end_times.append(clip.timeline_start + (clip.src_end - clip.src_start))
        return max(end_times)

    def __build_black_base(self, width: int, height: int, duration: float, filter_parts: list) -> str:
        """
        Makes the black canvas video for when there are empty space between clips.
        """
        label = "v_black_base"
        filter_parts.append(
            f"color=c=black:size={width}x{height}:duration={duration}:rate=30[{label}]"
        )
        return label

    def __build_layer(self, clips : list[ResolvedClip], filter_parts: list, width : int, height : int) -> tuple[str, str]:
        """
        Goes through all the videos and audio on a given layer and concatenates them.
        """
        stream_nodes = []
        
        # Without delaying our videos/audio, they by default start at t=0, which is not always what we want. 
        timeline_start = clips[0].timeline_start
        for clip in clips:
            video_label, audio_label = self.__build_clip_filters(
                clip=clip, 
                filter_parts=filter_parts,
                width=width,
                height=height)
            stream_nodes.append((video_label, audio_label))

        v_concat, a_concat = self.__build_concat(stream_nodes, filter_parts)
        uid = uuid4().hex[:6]
        v_out = f"v_delayed_{uid}"
        a_out = f"a_delayed_{uid}"
        
        delay_ms = int(timeline_start * 1000)
        filter_parts.append(
            f"[{v_concat}]setpts=PTS+{timeline_start}/TB[{v_out}]"
        )
        filter_parts.append(
            f"[{a_concat}]adelay={delay_ms}|{delay_ms}[{a_out}]"
        )

        return v_out, a_out

    def __build_clip_filters(self, clip: ResolvedClip, filter_parts: list, width :int, height : int) -> tuple[str, str]:
        """
        Filters in ffmpeg take in a media and apply some function to that given clip, this function is essentially compiling our DVEL clips into the corresponding FFMpeg clip.
        """
        index = self.__get_or_create_input_index(clip.path)
        uid = uuid4().hex[:6]
        video_label = f"v{index}_{uid}"
        audio_label = f"a{index}_{uid}"
        duration = clip.src_end - clip.src_start

        # If the clip is an audio clip, create a transparent video to place it over
        if clip.isAudio == True:
            filter_parts.append(
                f"color=c=black@0.0:size={width}x{height}:duration={duration}:rate=30,"
                f"format=yuva420p[{video_label}]"
            )
        else:
            # this is where we can add all of our effects to our video
            effect_chain = self.__build_effect_chain(clip.effects)

            filter_parts.append(
                f"[{index}:v]trim=start={clip.src_start}:end={clip.src_end},"
                f"setpts=PTS-STARTPTS,"
                # we are going to have to normalize each video, unfortunately adds compile time but it be what it be rn.
                f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
                f"fps=30,"
                f"format=yuv420p"
                f"{effect_chain}[{video_label}]"  # effects slot in here naturally
            )

        # Audio effect chain
        audio_effect_chain = self.__build_effect_chain(clip.effects)
        filter_parts.append(
            f"[{index}:a]atrim=start={clip.src_start}:end={clip.src_end},"
            # normalize our audio as well here
            f"asetpts=PTS-STARTPTS,"
            f"aresample=44100"
            f"{audio_effect_chain}[{audio_label}]"
        )
        return video_label, audio_label

    def __build_effect_chain(self, effects: list[Effect]) -> str:
        if not effects:
            return ""
        return "," + ",".join(self.__build_effect(e) for e in effects)

    def __build_effect(self, effect) -> str:
        """
        TODO:
        Make an EffectBuilder class that generates the effects
        This does nothing rn.
        """
        match effect.type:
            case "blur":
                pass
            case "saturation":
                pass
            case "speed":
                pass
            case "volume":
                return f"volume={effect.param[0]}"
            case _:
                raise Exception(f"Unknown effect: {effect.type}")
        return ""

    def __build_concat(self, stream_nodes: list, filter_parts: list) -> tuple[str, str]:
        """
        Given the nodes of a single layer, this function combines all of the media clips together.
        """
        uid: str = uuid4().hex[:6]
        v_out, a_out = f"v_layer_{uid}", f"a_layer_{uid}"
        inputs = "".join(f"[{v}][{a}]" for v, a in stream_nodes)
        filter_parts.append(
            f"{inputs}concat=n={len(stream_nodes)}:v=1:a=1[{v_out}][{a_out}]"
        )
        return v_out, a_out

    def __build_overlay_chain(self, base_v: str, layer_outputs: list, filter_parts: list) -> str:
        """
        Stacks the ffmpeg layers on top of each other.
        """
        current_v = base_v
        for i, (_, next_v, _) in enumerate(layer_outputs, start=1):
            out_v = f"v_overlay_{i}"
            # eof_action means when one layer is done we just keep playing with another playing layer instead of cutting off.
            filter_parts.append(f"[{current_v}][{next_v}]overlay=eof_action=pass[{out_v}]")
            current_v = out_v
        return current_v

    def __build_audio_mix(self, layer_outputs: list, filter_parts: list):
        """
        Audio builder, basically mixes our audio, nothing fancy, probably need to add audio effects at some point for volume at the very least.
        """
        audio_inputs = "".join(f"[{a}]" for _, _, a in layer_outputs)
        self.final_audio_label = "a_out"
        # amix is essentially overlay for audio
        filter_parts.append(
            f"{audio_inputs}amix=inputs={len(layer_outputs)}:duration=longest[{self.final_audio_label}]"
        )

    def build_text_overlay(self, text: str, timeline_start: float, duration: float, filter_parts: list, current_v: str) -> str:
        """
        Applies text element to the video frame.
        """
        uid = uuid4().hex[:6]
        out_label = f"v_text_{uid}"
        try:
            end_time = float(timeline_start) + float(duration)
        except ValueError:
            raise Exception(f"You must explicitly define the start time of the text string:{text}")

        filter_parts.append(
            f"[{current_v}]drawtext="
            f"text='{text}':"
            f"fontfile='C\\:/Windows/Fonts/arial.ttf':"
            f"fontsize=56:" # Font size 56
            f"fontcolor=white:"
            f"x=(w-text_w)/2:" # Centered in the screen
            f"y=(h-text_h-50):" # 50 pixels from the bottom of screen
            f"enable='between(t, {float(timeline_start):.3f}, {end_time:.3f})'"
            f"[{out_label}]"
        )
        return out_label