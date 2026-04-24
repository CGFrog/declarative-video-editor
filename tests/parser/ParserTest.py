from src.compiler.parser.RenderSettings import RenderSettings
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.StateVariable import StateVariable
from src.compiler.StateVariable import Clip, Effect
from src.compiler.parser.Parser import Parser

TEST1 : str =  """
num n1 = 5.0
video intro = \"intro.mp4\" (0,e) |> saturation(n1) |> speed(1.5)            
timeline
intro 0 1
% Hey this is a comment      
render \"lets_play.mp4\" [1920,1080] % Comment time!
"""

introVar: StateVariable = StateVariable()
introVar.effects.append(
    Effect(
        'speed', 
        ['1.5']
    )
)

introVar.effects.append(
    Effect(
        'saturation', 
        ['5.0'])
    )
introVar.clips.append(
    Clip(
        "intro.mp4", 
        ['0','e']
        )
    )

state: dict[str, StateVariable] = {
    "intro" : introVar,
}

timeline: list[TimelineElement] = [
    TimelineElement(
        identifier = "intro", 
        start_time='0',z='1'
    )
]

render_settings = RenderSettings(
    export_path="lets_play.mp4",
    resolution= ("1920","1080")
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

# --- Expected state for TEST2 --- #
v1Var: StateVariable = StateVariable()
v1Var.clips.append(Clip("v1.mp4", ['0', 'e']))
v1Var.effects.append(Effect('saturation', ['1']))
v1Var.effects.append(Effect('speed', ['2']))
v1Var.effects.append(Effect('volume', ['3']))


v2Var: StateVariable = StateVariable()
v2Var.clips.append(Clip("v2.mp4", ['0', 'e']))
v2Var.effects.append(Effect('saturation', ['3']))
v2Var.effects.append(Effect('speed', ['1']))
v2Var.effects.append(Effect('volume', ['2']))

state2: dict[str, StateVariable] = {
    "v1": v1Var,
    "v2": v2Var,
}

render_settings2 = RenderSettings(
    export_path="output.mp4",
    resolution=("1920","1080")
)

timeline2: list[TimelineElement] = [
    TimelineElement(identifier="v1", start_time='0', z='1'),
    TimelineElement(identifier="v2", start_time='0', z='2')
]


if __name__=="__main__":
    """
    Duplicating code, TODO, add a testcase
    parent class all future 
    test case inherit from.
    """
    parser = Parser()
    parser.parse_source(TEST1)
    assert parser.state == state
    assert parser.timeline == timeline
    assert parser.render_settings == render_settings
    assert parser.primitives == {"n1" : 5.0}

     # TEST2
    parser2 = Parser()
    parser2.parse_source(TEST2)
    assert parser2.state == state2
    assert parser2.timeline == timeline2
    assert parser2.render_settings == render_settings2