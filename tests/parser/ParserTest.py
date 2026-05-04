import sys
from src.compiler.parser.RenderSettings import RenderSettings
from src.compiler.parser.TimelineElement import TimelineElement
from src.compiler.VideoVariable import Clip, VideoVariable
from src.compiler.Effect import Effect
from src.compiler.parser.Parser import Parser


"""
NOTE FOR BRIAN: Used AI to generate these test cases, did not want to do this by hand.
"""

TEST1 = """
num n1 = 5.0;
video intro = "intro.mp4" (0,e) |> saturation(n1) |> speed(1.5);
timeline
intro 0 1
render "lets_play.mp4" [1920,1080]
"""

expected_state1 = {
    "intro": VideoVariable(
        clips=[Clip("intro.mp4", ['0', 'e'])],
        effects=[
            Effect('speed', ['1.5']),
            Effect('saturation', ['5.0']),
        ],
        type="video"
    )
}

expected_timeline1 = [
    TimelineElement("intro", '0', '1')
]

expected_render1 = RenderSettings("lets_play.mp4", ("1920", "1080"))
expected_primitives1 = {"n1": '5.0'}


TEST2 = """
func f(a,b,c) = saturation(a) |> speed(b) |> volume(c);
video v1 = "v1.mp4" (0,e) |> f(1,2,3);
video v2 = "v2.mp4" (0,e) |> f(3,1,2);
timeline
v1 0 1
v2 0 2
render "output.mp4" [1920,1080]
"""

expected_state2 = {
    "v1": VideoVariable(
        clips=[Clip("v1.mp4", ['0', 'e'])],
        effects=[
            Effect('volume', ['3']),
            Effect('speed', ['2']),
            Effect('saturation', ['1']),
        ],
        type="video"
    ),
    "v2": VideoVariable(
        clips=[Clip("v2.mp4", ['0', 'e'])],
        effects=[
            Effect('volume', ['2']),
            Effect('speed', ['1']),
            Effect('saturation', ['3']),
        ],
        type="video"
    ),
}

expected_timeline2 = [
    TimelineElement("v1", '0', '1'),
    TimelineElement("v2", '0', '2')
]

expected_render2 = RenderSettings("output.mp4", ("1920", "1080"))

def get_test(test_num: int):
    match test_num:
        case 1:
            return TEST1, expected_state1, expected_timeline1, expected_render1, expected_primitives1
        case 2:
            return TEST2, expected_state2, expected_timeline2, expected_render2, None
        case _:
            raise Exception("Unknown Test")

def run_parser(source: str):
    parser = Parser()
    parser.parse_source(source)
    return parser

def compare(name, expected, actual):
    if expected != actual:
        print(f"\n {name} FAILED")
        print("----- EXPECTED -----")
        print(expected)
        print("----- GOT ----------")
        print(actual)
        print("--------------------\n")
        return False
    else:
        print(f"{name} passed")
        return True

if __name__ == "__main__":
    test_num = int(sys.argv[1])

    source, exp_state, exp_timeline, exp_render, exp_primitives = get_test(test_num)
    parser = run_parser(source)

    ok = True
    ok &= compare("STATE", exp_state, parser.state)
    ok &= compare("TIMELINE", exp_timeline, parser.timeline)
    ok &= compare("RENDER SETTINGS", exp_render, parser.render_settings)

    if exp_primitives is not None:
        ok &= compare("PRIMITIVES", exp_primitives, parser.primitives)

    if ok:
        print("\nTEST PASSED")
    else:
        raise AssertionError("TEST FAILED")