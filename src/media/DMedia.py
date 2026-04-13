import ffmpeg
import abc
import uuid

class DMedia():
    """
    Base class for Audio, Images, and Videos.
    Serves as a wrapper over the ffmpeg files we will be modifying.

    Constructor Args:
        name: DVEL media variable name.
        file_path: path to file
    """
    def __init__(self, name : str, file_path : str) -> None:
        self.name = name
        self.file_path = file_path
        self.duration: str = ""
        self.cache_path = f"cache/name_{uuid.uuid4()}.mp4"
        ffmpeg.input(self.file_path).output(self.cache_path).run()
    
    @classmethod
    def trim(self, time1, time2)->None:
        pass

    @classmethod
    def union(self, media)->None:
        pass

    @classmethod
    def overlay(self, media)->None:
        pass