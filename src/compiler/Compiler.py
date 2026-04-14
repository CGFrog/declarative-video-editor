from pathlib import Path
from sre_parse import State
from uuid import uuid4
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
        self.cached_videos: dict[str, DMedia] = self.__generate_medias(state=self.state)


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
            match media_data.type:
                case "audio":
                    pass
                case "img":
                    pass
                case "video":
                    output_path: str = f"cache/{media_data.type.strip()}_{uuid4()}"
                    self.__generate_video(
                        path=output_path,
                        media_data = media_data
                    )
    
    def __generate_video(self, path, media_data : StateVariable):
        

    def __render(self):
        pass