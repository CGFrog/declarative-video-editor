   
class TimelineVariable:
        def __init__(self, file_path: str, start_time: str, end_time: str):
            self.cache_file = file_path
            self.start_time = start_time
            self.end_time = end_time