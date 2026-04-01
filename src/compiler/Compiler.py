from pathlib import Path

def Compiler():
    def compile(output : str):
        generateFolders()        

    def generateFolders():
        """
        Generates folders that hold the output video files and the intermediary video files that create the final output.
        """
        folder_path = Path("output")
        folder_path.mkdir(parents=True, exist_ok=True)
        folder_path = Path("cache")
        folder_path.mkdir(parents=True, exist_ok=True)
    
    
    
    class StateVariable:
        def __init__(self, clip : tuple):
            self.effects: list[Effect] = []
            self.clips = clip 
            self.duration: str | None = None #timestamp

        def add_effect(self, effect):
            self.effects.append(effect)
        
        def set_duration(self, timestamp: str):
            self.duration = timestamp
    

    class Effect:
        def __init__(self, param: tuple):
            self.param = param
            pass      
    
    '''
    Effect types are done through inheritance

    '''

    class Blur(Effect):
        def __init__(self):
            super().__init__()

    class Saturation(Effect): 
        def __init__(self):
            super().__init__()
        
    class Chroma(Effect):
        def __init__(self):
            super().__init__()

    class Transform(Effect):
        def __init__(self):
            super().__init__()
        
    class Scale(Effect):
        def __init__(self):
            super().__init__()
        
    class NoiseFilter(Effect):
        def __init__(self):
            super().__init__()
        
    class Volume(Effect):
        def __init__(self):
            super().__init__()

    class Speed(Effect):
        def __init__(self):
            super().__init__()


    class TimelineVariable:
        def __init__(self, file_path: str, start_time: str, end_time: str):
            self.cache_file = file_path
            self.start_time = start_time
            self.end_time = end_time
            #...
