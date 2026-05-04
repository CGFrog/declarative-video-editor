import math
from src.compiler.Effect import Effect

class EffectBuilder:
    
    def build(self, effect: Effect) -> str:

        if effect.type == "volume":
            return ""
        
        match effect.type:
            case "blur":
                return self._build_blur(effect)
            case "saturation":
                return self._build_saturation(effect)
            case "speed":
                return self._build_speed(effect)
            case "location":
                return self._build_location(effect)
            case "scale":
                return self._build_scale(effect)
            case "rotation":
                return self._build_rotation(effect)
            case "crop":
                return self._build_crop(effect)
            case "colorkey":
                return self._build_colorkey(effect)
            case _:
                raise Exception(f"Unknown effect: {effect.type}")

    def get_audio_filter(self, effect: Effect) -> str:
        if effect.type == "speed":
            speed = effect.param[0] if len(effect.param) > 0 else 1.0
            return f"atempo={speed}"
        if effect.type == "volume":
            volume = effect.param[0] if len(effect.param) > 0 else 1.0
            return f"volume={volume}"
        return ""
    
    def _build_blur(self, effect: Effect) -> str:
        radius = effect.param[0] if len(effect.param) > 0 else 5
        return f"boxblur={radius}:1"
    
    def _build_saturation(self, effect: Effect) -> str:
        saturation = effect.param[0] if len(effect.param) > 0 else 1.0
        return f"hue=s={saturation}"
    
    def _build_speed(self, effect: Effect) -> str:
        speed = float(effect.param[0]) if len(effect.param) > 0 else 1.0
        if not (0.5 <= speed <= 2.0):
            raise Exception(f"Speed must be between 0.5 and 2.0, got {speed}")
        pts_factor = round(1.0 / speed, 6)
        return f"setpts={pts_factor}*PTS"

    def _build_location(self, effect: Effect) -> str:
        x = effect.param[0] if len(effect.param) > 0 else 0
        y = effect.param[1] if len(effect.param) > 1 else 0
        resolution_w = effect.param[2] if len(effect.param) > 2 else "iw"
        resolution_h = effect.param[3] if len(effect.param) > 3 else "ih"
        return f"pad={resolution_w}:{resolution_h}:{x}:{y}"

    def _build_scale(self, effect: Effect) -> str:
        pct = effect.param[0] if len(effect.param) > 0 else 1.0
        return f"scale=iw*{pct}:ih*{pct}"

    def _build_rotation(self, effect: Effect) -> str:
        angle_deg = float(effect.param[0]) if len(effect.param) > 0 else 0.0
        angle_rad = round(angle_deg * math.pi / 180, 6)
        return f"rotate={angle_rad}"

    def _build_crop(self, effect: Effect) -> str:
        """
        crop(1280, 720)      → crops to 1280x720 from top-left corner
        crop(1280, 720, 100) → crops to 1280x720 starting at x=100, y=0
        crop(1280, 720, 100, 50) → crops to 1280x720 starting at x=100, y=50
        """
        width = effect.param[0] if len(effect.param) > 0 else "iw"
        height = effect.param[1] if len(effect.param) > 1 else "ih"
        x_offset = effect.param[2] if len(effect.param) > 2 else 0 
        y_offset = effect.param[3] if len(effect.param) > 3 else 0
        return f"crop={width}:{height}:{x_offset}:{y_offset}"

    def _build_colorkey(self, effect: Effect) -> str:
        color = effect.param[0] if len(effect.param) > 0 else "0x00FF00"
        similarity = effect.param[1] if len(effect.param) > 1 else 0.3
        blend = effect.param[2] if len(effect.param) > 2 else 0.1
        return f"colorkey={color}:{similarity}:{blend}"