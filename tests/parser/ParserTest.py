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
        ['5'])
    )
introVar.clips.append(
    Clip(
        "intro.mp4", 
        ['0','e']
        )
    )

state: dict[str, StateVariable] = {
    "intro" : introVar,
    "n1" : 5.0
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