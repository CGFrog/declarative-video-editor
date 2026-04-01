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

    def location(self, new_x : float, new_y : float, resolution_w : float, resolution_h : float):
        """
        Moves the x, y coordinates of the anchor point of a video:
        Args:
            new_x: x coordinate of the video's anchor point
            new_y: y coordinate of the video's anchor point
            resolution_w: video "canvas" width
            resolution_h: video "canvas" height
        """
        ffmpeg.input(self.cache_path).filter('pad', w=resolution_w, h=resolution_h, new_x=new_x, new_y=new_y).output(self.cache_path).run()

    def rotation(self, angle : float):
        """
        Rotates the video clockwise by degrees:
        Args:
            angle: degree amount to rotate video by
        """
        ffmpeg.input(self.cache_path).filter('rotate', rotation_angle=(angle * math.pi / 180)).output(self.cache_path).run()

    def scale(self, pct : float):
        """
        Increases/decreases the size (length & width) of the video
        Args:
            pct: percentage increase/decrease in the video's scale
        """
        scale = f'iw*{pct}:ih*{pct}'
        ffmpeg.input(self.cache_path).filter('scale', scale_pct=scale).output(self.cache_path).run()

    def crop(self, width : float, height : float, x_offset : float, y_offset : float):
        """
        Cut content from the video frame (width & height)
        Args:
            width: cropped area of video width
            height: cropped area of video height
            x_offset: amount of pixels to crop from the x-axis
            y_offset: amount of pixels to crop from the y-axis
        """
        ffmpeg.input(self.cache_path).filter('crop', width=width, height=height, x_off=x_offset, y_off=y_offset).output(self.cache_path).run()

    def overlay(self, media):
        pass