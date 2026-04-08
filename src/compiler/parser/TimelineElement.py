class TimelineElement:
    def __init__(self, identifier: str,  start_time : str, z : str):
        # Might be worth converting these to better types here i.e. timestamps and ints.
        self.identifier = identifier
        self.start_time: str = start_time
        self.z: str = z
