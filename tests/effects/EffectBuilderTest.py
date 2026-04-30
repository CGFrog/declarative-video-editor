from src.compiler.Effect import Effect
from src.compiler.EffectBuilder import EffectBuilder

builder = EffectBuilder()

# Test saturation
effect = Effect("saturation", [5.0])
print(builder.build(effect))  

# Test speed video side
effect = Effect("speed", [2.0])
print(builder.build(effect))  

# Test speed audio side
print(builder.get_audio_filter(effect)) 

# Test blur
effect = Effect("blur", [10])
print(builder.build(effect)) 