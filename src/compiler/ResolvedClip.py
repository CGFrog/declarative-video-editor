class ResolvedClip:
    def __init__(self, path, src_start, src_end, timeline_start, z, effects):
        self.path = path
        self.src_start = src_start
        self.src_end = src_end
        self.timeline_start = timeline_start
        self.z = z
        self.effects = effects
