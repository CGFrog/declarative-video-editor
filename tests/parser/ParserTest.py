from src.compiler.parser.RenderSettings import RenderSettings
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.VideoVariable import Clip, VideoVariable
from src.compiler.StateVariable import StateVariable
from src.compiler.Effect import Effect
from src.compiler.parser.Parser import Parser

TEST1: str = """
num n1 = 5.0
video intro = "intro.mp4" (0,e) |> saturation(n1) |> speed(1.5)            
timeline
intro 0 1
% Hey this is a comment      
render "lets_play.mp4" [1920,1080] % Comment time!
"""



introVar = VideoVariable(
    clips=[
        Clip("intro.mp4", ['0', 'e'])
    ],
    effects=[
        Effect('speed', ['1.5']),
        Effect('saturation', ['5.0']),
    ],
    type="video"
)

state = {
    "intro": introVar,
}

timeline = [
    TimelineElement(
        identifier="intro",
        start_time='0',
        z='1'
    )
]

render_settings = RenderSettings(
    export_path="lets_play.mp4",
    resolution=("1920", "1080")
)

TEST2: str = """
func f(a,b,c) = saturation(a) |> speed(b) |> volume(c)
video v1 = "v1.mp4" (0,e) |> f(1,2,3)
video v2 = "v2.mp4" (0,e) |> f(3,1,2)
timeline
v1 0 1
v2 0 2
render "output.mp4" [1920,1080]
"""

v1Var = VideoVariable(
    clips=[Clip("v1.mp4", ['0', 'e'])],
    effects=[
        Effect('volume', ['3']),
        Effect('speed', ['2']),
        Effect('saturation', ['1']),
    ],
    type="video"
)

v2Var = VideoVariable(
    clips=[Clip("v2.mp4", ['0', 'e'])],
    effects=[
        Effect('volume', ['2']),
        Effect('speed', ['1']),
        Effect('saturation', ['3']),
    ],
    type="video"
)

state2 = {
    "v1": v1Var,
    "v2": v2Var,
}

timeline2 = [
    TimelineElement(identifier="v1", start_time='0', z='1'),
    TimelineElement(identifier="v2", start_time='0', z='2')
]

render_settings2 = RenderSettings(
    export_path="output.mp4",
    resolution=("1920", "1080")
)
if __name__ == "__main__":
    parser = Parser()
    parser.parse_source(TEST1)

    assert parser.state == state
    assert parser.timeline == timeline
    assert parser.render_settings == render_settings
    assert parser.primitives == {"n1": '5.0'}

    parser2 = Parser()
    parser2.parse_source(TEST2)

    print(parser2.state)
    print(state2)
    assert parser2.state == state2
    assert parser2.timeline == timeline2
    assert parser2.render_settings == render_settings2

    print("All tests passed.")