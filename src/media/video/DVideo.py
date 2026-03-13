from src.media.DMedia import DMedia

class DVideo(DMedia): #D just seems like a reasonable way to distinguish between our video wrapper class and the ffmpeg video class. I.e. the D in DVET.
    def __init__(self, name : str, file_path : str)-> None:
        super()

    def trim(start : str, duration :str):
        """
        Trims a video starting at a specific time in seconds throughout a given duration:
        Args:
            start: Start time of trim in seconds
            duration: Duration of trim in seconds
        """
        ffmpeg.input(self.cache_path, ss=start, duration=duration).output(cache_path).run()

    def concat():
        pass