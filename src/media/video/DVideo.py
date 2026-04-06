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
        # Generate new path to avoid reading/writing to same file
        new_version_path = self.generate_temp_path()
        
        # Load two video files 
        v1 = ffmpeg.input(self.cache_path)
        v2 = ffmpeg.input(media.cache_path)

        # Grab audio and video streams from V1 and V2 --> Concatenate them!
        joined = ffmpeg.concat(v1.video, v1.audio, v2.video, v2.audio, v=1, a=1).node

        # Output final video
        (
            ffmpeg
            .output(joined[0], joined[1], new_version_path)
            .run()
        )
        
        self.cache_path = new_version_path
        

    def overlay(self, media):
        pass


    def colorkey(self, media):
        # Generate new path to avoid reading/writing to same file
        new_version_path = self.generate_temp_path()

        foreground = ffmpeg.input(self.cache_path)
        background = ffmpeg.input(media.cache_path)

        # Apply filter
        keyed_video = foreground.video.filter("colorkey", "0x00FF00", 0.3, 0.1)

        # Overlay the video onto background
        final_video = ffmpeg.overlay(background.video, keyed_video)

        # Output final video along with audio from original video
        (
            ffmpeg
            .output(final_video, foreground.audio, new_version_path)
            .run()
        )

        self_cache_path = new_version_path
