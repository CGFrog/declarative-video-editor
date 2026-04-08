class RenderSettings:
    def __init__(self, export_path : str, resolution: tuple[str,str]):
        self.x: str = resolution[0]
        self.y: str = resolution[1]
        self.export_path = export_path
