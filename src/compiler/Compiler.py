from pathlib import Path
from uuid import uuid4
import uuid
from src.media.video.DVideo import DVideo
from src.media.DMedia import DMedia
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.StateVariable import StateVariable
from src.compiler.parser.Parser import Parser

class Compiler():
    def compile(self,source_code: str):
        parser = Parser()
        parser.parse_source(source_code=source_code)
        self.state: dict[str, StateVariable] = parser.state
        self.timeline: list[TimelineElement] = parser.timeline
        self.cached_videos: dict[str, DMedia] = {} 
        self.__generate_medias(state=self.state)


    def __generate_folders(self):
        """
        Generates folders that hold the output video files and the intermediary video files that create the final output.
        """
        folder_path = Path("output")
        folder_path.mkdir(parents=True, exist_ok=True)
        folder_path = Path("cache")
        folder_path.mkdir(parents=True, exist_ok=True)

    def __generate_medias(self, state: dict[str,StateVariable]):
        for media in self.state.items():
            media_name: str = media[0]
            media_data: StateVariable = media[1]
            match media_data.type: # must add audio types and I guess image but maybe a way to treat images as single frame videos idk.
                case "video":
                    self.cached_videos.update({media_name :self.__generate_video(media_data = media_data)})

            
    def __generate_video(self, media_data : StateVariable): 
        video = None
        for clip in media_data.clips:
            current_clip = DVideo(clip.path)
            current_clip.trim(clip.duration[0],clip.duration[1])
            if video is not None:
                video.union(current_clip)
            else:
                video = current_clip
        if video == None:
            raise Exception("No clips were declared in DVEL code that are able to render.")
        print(f"video cached at :{video.cache_path}")
        return video
    

    def __calculate_duration(self):
        pass

    def __apply_effects(self):
        pass

    def __render(self) -> None:
        pass

def main():
    source_code =   """video intro = \"intro.mp4\" (0,e) |> saturation(3) |> speed(1.5)
                audio music = \"music.mp3\" (0,e) |> volume(2) |> noise_filter(-60)
                video game_footage = \"game_footage.mp4\" (0,30) + (35,49)
                video webcam_footage = \"webcam_footage.mp4\" (0,30) + (35,49) |> transform(1000,320) |> scale(0.2,0.2)
                
                
                timeline
                intro 0 1
                game_footage after intro 1
                music 0 1
                webcam_footage after intro 2
                
                render \"lets_play.mp4\" [1920,1080]"""
    compiler = Compiler()
    compiler.compile(source_code=source_code)

if __name__ == "__main__":
    main()
