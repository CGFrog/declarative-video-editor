from uuid import uuid4

class FFMpegBuilder:
    def __init__(self):
        self.input_index: dict[str, int] = {}
        self.next_index: int = 0
        self.final_video_label: str = ""

    def __get_or_create_input_index(self, path: str) -> int:
        if path not in self.input_index:
            self.input_index[path] = self.next_index
            self.next_index += 1
        return self.input_index[path]

    def build_inputs(self) -> str:
        sorted_inputs = sorted(self.input_index.items(), key=lambda x: x[1])
        return " ".join(f'-i "{path}"' for path, _ in sorted_inputs)

    def build_filter_graph(self, layers, width: int, height: int) -> str:
        filter_parts = []
        layer_outputs = []
        duration = self.__get_total_duration(layers)

        black = self.__build_black_base(width, height, duration, filter_parts)

        for z in sorted(layers.keys()):
            v_out, a_out = self.__build_layer(layers[z], filter_parts)
            layer_outputs.append((z, v_out, a_out))

        self.final_video_label = self.__build_overlay_chain(black, layer_outputs, filter_parts)
        self.__build_audio_mix(layer_outputs, filter_parts)

        return ";".join(filter_parts)

    def __get_total_duration(self, layers) -> float:
        end_times = []
        for clips in layers.values():
            for clip in clips:
                end_times.append(clip.timeline_start + (clip.src_end - clip.src_start))
        return max(end_times)

    def __build_black_base(self, width: int, height: int, duration: float, filter_parts: list) -> str:
        label = "v_black_base"
        filter_parts.append(
            f"color=c=black:size={width}x{height}:duration={duration}:rate=30[{label}]"
        )
        return label

    def __build_layer(self, clips, filter_parts: list) -> tuple[str, str]:
        stream_nodes = []
        for clip in clips:
            video_label, audio_label = self.__build_clip_filters(clip, filter_parts)
            stream_nodes.append((video_label, audio_label))
        return self.__build_concat(stream_nodes, filter_parts)

    def __build_clip_filters(self, clip, filter_parts: list) -> tuple[str, str]:
        index = self.__get_or_create_input_index(clip.path)
        uid = uuid4().hex[:6]
        video_label = f"v{index}_{uid}"
        audio_label = f"a{index}_{uid}"
        delay_ms = int(clip.timeline_start * 1000)

        filter_parts.append(
            f"[{index}:v]trim=start={clip.src_start}:end={clip.src_end},"
            f"setpts=PTS-STARTPTS+{clip.timeline_start}/TB[{video_label}]"
        )
        filter_parts.append(
            f"[{index}:a]atrim=start={clip.src_start}:end={clip.src_end},"
            f"asetpts=PTS-STARTPTS,adelay={delay_ms}|{delay_ms}[{audio_label}]"
        )

        return video_label, audio_label

    def __build_concat(self, stream_nodes: list, filter_parts: list) -> tuple[str, str]:
        uid = uuid4().hex[:6]
        v_out, a_out = f"v_layer_{uid}", f"a_layer_{uid}"
        inputs = "".join(f"[{v}][{a}]" for v, a in stream_nodes)
        filter_parts.append(
            f"{inputs}concat=n={len(stream_nodes)}:v=1:a=1[{v_out}][{a_out}]"
        )
        return v_out, a_out

    def __build_overlay_chain(self, base_v: str, layer_outputs: list, filter_parts: list) -> str:
        current_v = base_v
        for i, (_, next_v, _) in enumerate(layer_outputs, start=1):
            out_v = f"v_overlay_{i}"
            filter_parts.append(f"[{current_v}][{next_v}]overlay=eof_action=pass[{out_v}]")
            current_v = out_v
        return current_v

    def __build_audio_mix(self, layer_outputs: list, filter_parts: list):
        audio_inputs = "".join(f"[{a}]" for _, _, a in layer_outputs)
        filter_parts.append(
            f"{audio_inputs}amix=inputs={len(layer_outputs)}:duration=longest[a]"
        )