from src.media.DMedia import DMedia
import ffmpeg
import math

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

    def location(self, x : float, y : float):
        """
        Moves the x, y coordinates of the anchor point of a video:
        Args:
            x: x coordinate of the video's anchor point
            y: y coordinate of the video's anchor point
        """
        v = ffmpeg.input(self.cache_path)
        ffmpeg.overlay(self.cache_path, v, x, y).output(self.cache_path).run()

    def rotation(self, angle : float):
        """
        Rotates the video clockwise by degrees:
        Args:
            angle: degree amount to rotate video by
        """
        ffmpeg.input(self.cache_path).filter('rotate', angle * math.pi / 180).output(self.cache_path).run()

    def scale(self, pct : float):
        """
        Increases/decreases the size (length & width) of the video
        Args:
            pct: percentage increase/decrease in the video's scale
        """
        scale = f'iw*{pct}:ih*{pct}'
        ffmpeg.input(self.cache_path).filter('scale', scale).output(self.cache_path).run()

    def crop(self, width, height, x_offset, y_offset):
        """
        Cut content from the video frame (width & height)
        Args:
            width: cropped video width
            height: cropped video height
            x_offset: amount of pixels to crop from the x-axis
            y_offset: amount of pixels to crop from the y-axis
        """
        ffmpeg.input(self.cache_path).filter('crop', width, height, x_offset, y_offset).output(self.cache_path).run()

    def overlay(self, media):
        pass