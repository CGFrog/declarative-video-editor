import ffmpeg
from src.compiler.CompilerUtils import generate_temp_path

class DMedia():
    """
    Base class for Audio, Images, and Videos.
    Serves as a wrapper over the ffmpeg files we will be modifying.

    Constructor Args:
        name: DVEL media variable name.
        file_path: path to file
    """
    def __init__(self, file_path : str) -> None:
        self.file_path = file_path
        self.duration: str = ""
        self.cache_path = generate_temp_path()
        ffmpeg.input(self.file_path).output(self.cache_path).run()
    
    @classmethod
    def trim(cls, self, time1, time2)->None:
        pass

    @classmethod
    def union(cls, self, media)->None:
        pass

    @classmethod
    def overlay(cls, self, media)->None:
        pass