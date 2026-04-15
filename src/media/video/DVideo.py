from uuid import uuid4
from src.media.DMedia import DMedia
import ffmpeg
import math
from src.compiler.CompilerUtils import generate_temp_path

class DVideo(DMedia): #D just seems like a reasonable way to distinguish between our video wrapper class and the ffmpeg video class. I.e. the D in DVEL.
    def __init__(self, file_path : str)-> None:
        super().__init__(file_path)

    def trim(self, start : str, duration :str):
        """
        Trims a video starting at a specific time in seconds throughout a given duration:
        Args:
            start: Start time of trim in seconds
            duration: Duration of trim in seconds
        """
        new_path:str = generate_temp_path()
        if duration == 'e':
            ffmpeg.input(self.cache_path, ss=start).output(new_path, c='copy').run()
        else:
            ffmpeg.input(self.cache_path, ss=start, t=duration).output(new_path).run()
        self.cache_path = new_path

    def union(self, media):
        # Generate new path to avoid reading/writing to same file
        new_path:str = generate_temp_path()
        
        # Load two video files 
        v1 = ffmpeg.input(self.cache_path)
        v2 = ffmpeg.input(media.cache_path)

        # Grab audio and video streams from V1 and V2 --> Concatenate them!
        v3 = ffmpeg.concat(v1.video, v1.audio, v2.video, v2.audio, v=1, a=1).node

        # Output final video
        (
            ffmpeg
            .output(v3[0], v3[1], new_path)
            .run()
        )
        
        self.cache_path = new_path

    def location(self, new_x : float, new_y : float, resolution_w : float, resolution_h : float):
        """
        Moves the x, y coordinates of the anchor point of a video:
        Args:
            new_x: x coordinate of the video's anchor point
            new_y: y coordinate of the video's anchor point
            resolution_w: video "canvas" width
            resolution_h: video "canvas" height
        """
        new_path = generate_temp_path()
        (        
            ffmpeg
            .input(self.cache_path)
            .filter('pad', w=resolution_w, h=resolution_h, new_x=new_x, new_y=new_y)
            .output(new_path).run()
        )
        self.cache_path = new_path

    def rotation(self, angle : float):
        """
        Rotates the video clockwise by degrees:
        Args:
            angle: degree amount to rotate video by
        """
        new_path = generate_temp_path()
        (
            ffmpeg
            .input(self.cache_path)
            .filter('rotate', rotation_angle=(angle * math.pi / 180))
            .output(new_path).run()
        )
        self.cache_path=new_path

    def scale(self, pct : float):
        """
        Increases/decreases the size (length & width) of the video
        Args:
            pct: percentage increase/decrease in the video's scale
        """
        new_path = generate_temp_path()
        scale = f'iw*{pct}:ih*{pct}'
        (
            ffmpeg.input(self.cache_path).filter('scale', scale_pct=scale).output(new_path).run()
        )
        self.cache_path=new_path

    def crop(self, width : float, height : float, x_offset : float, y_offset : float):
        """
        Cut content from the video frame (width & height)
        Args:
            width: cropped area of video width
            height: cropped area of video height
            x_offset: amount of pixels to crop from the x-axis
            y_offset: amount of pixels to crop from the y-axis
        """
        new_path = generate_temp_path()
        (
            ffmpeg.input(self.cache_path).filter('crop', width=width, height=height, x_off=x_offset, y_off=y_offset).output(new_path).run()
        )
        self.cache_path = new_path

    def overlay(self, media):
        pass


    def colorkey(self, media, color="0x00FF00", similarity = 0.3, blend = 0.1):
        """
        Apply colorkey filter using color of choice
        Args:
            Color (string): Hexadecimal value of color of your background you want to be transparent

            Similarity: Float 0 to 1 that represents how close a pixel has to be to color
            variable for it to be included in filter

            Blend: Float 0 to 1 that represents how smooth the edges are of the green screen.
            Lower the number the more jagged they may look while the higher the number may 
            produce a "blurry" or "faded" effect. 
        """
        
        # Generate new path to avoid reading/writing to same file
        new_path:str = generate_temp_path()

        foreground = ffmpeg.input(self.cache_path)
        background = ffmpeg.input(media.cache_path)

        # Apply filter
        keyed_video = foreground.video.filter("colorkey", color, similarity, blend)

        # Overlay the video onto background
        final_video = ffmpeg.overlay(background.video, keyed_video)

        # Output final video along with audio from original video
        ffmpeg.output(final_video, foreground.audio, new_path).run()

        self.cache_path = new_path

