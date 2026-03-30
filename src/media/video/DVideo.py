from src.media.DMedia import DMedia
import ffmpeg

class DVideo(DMedia): #D just seems like a reasonable way to distinguish between our video wrapper class and the ffmpeg video class. I.e. the D in DVET.
    def __init__(self, name : str, file_path : str)-> None:
        super()

    def trim(self, start : str, duration :str):
        """
        Trims a video starting at a specific time in seconds throughout a given duration:
        Args:
            start: Start time of trim in seconds
            duration: Duration of trim in seconds
        """
        ffmpeg.input(self.cache_path, ss=start, duration=duration).output(cache_path).run()

    def union(self, media):
        
        # Load two video files 
        v1 = ffmpeg.input(self.cache_path)
        v2 = ffmpeg.input(media.cache_path)

        # Grab audio and video streams from V1 and V2 --> Concatenate them!
        v3 = ffmpeg.concat(v1.video, v1.audio, v2.video, v2.audio, v=1, a=1)

        # Output final video
        ffmpeg.output(v3[0], v3[1], self.cache_path).run()

    def location(self, x, y):

        # Load video file
        v = ffmpeg.input(self.cache_path)

        pass

    def rotation(self, angle_deg):
        pass

    def scale(self, pct):
        pass

    def crop(self, width, height, x_offset, y_offset):
        pass

    def overlay(self, media):
        pass