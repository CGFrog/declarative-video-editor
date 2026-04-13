class TimelineElement:
    def __init__(self, identifier: str,  start_time : str, z : str):
        # Might be worth converting these to better types here i.e. timestamps and ints.
        self.identifier = identifier
        self.start_time: str = start_time
        self.z: str = z

    def __eq__(self, other)-> bool:
        if isinstance(other, TimelineElement):
            return self.identifier == other.identifier and self.start_time == other.start_time and self.z == other.z 
        return False