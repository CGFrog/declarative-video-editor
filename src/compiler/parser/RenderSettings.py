class RenderSettings:
    def __init__(self, export_path : str, resolution: tuple[str,str]):
        self.x: str = resolution[0]
        self.y: str = resolution[1]
        self.export_path = export_path

    def __eq__(self, other)->bool:
        if isinstance(other, RenderSettings):
            return self.x == other.x and self.y == other.y and self.export_path == other.export_path
        return False