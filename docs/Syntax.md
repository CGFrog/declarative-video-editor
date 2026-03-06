<h1>Syntax</h1>

We declare a variable with the following syntax:
```
video v_1 = "intro.mp4" (0,0:45)
<type> <name> = <path/var> <duration> <additional info>
```

This can be read as, create a video called v_1 that is the first 45 seconds of `intro.mp4`.

We can similarly do the same for audio and images:

> [!NOTE]
> Use `hh:mm:ss.ms` or `mm:ss.ms` or `ss.ms` or `ss` format for time. 

```
audio a_1 = "epic_song.mp3" (0,1:45.42)
image i_1b = "cat.png" (0,34.4)
```
> [!NOTE]
> Images have duration as well.
> 
Use `(t_1,e)` to indicate we start at `t_1` and end at the video's end. 
<h3> Union </h3>

Potentially, we may wish to import several cuts from a video and merge them into the same clip; we can define a media union operator `+`.
```
video v_2 = "lecture.mp4" (0,1:12:15) + (1:13:52,1:14:01)
```
We can use the union operator on two videos as well:
```
video v_3 = v_1 + v_2
```

<h3> Trim </h3>

The trim operator `(t_1,t_2)` tells us what time portion of the media it is that we want. This means we want all of the video from time `t_1` to time `t_2`.
Perhaps we want to cut something out of the video, then we define the complement of trim as `!(t_1,t_2)`. That is, for a video of length 60s, `!(10,25)` will produce `(0,10)+(25,60)`.

<h3> Pipe </h3>

We define the `pipe` operator `|>` as an operator that uses function composition to add effects to our video

```
video v_1 = "cool_video.mp4" (0,e) |> blur(5) |> saturation(5)
<var name> |> <last effect> |> ... |> <first effect>

# this is similar to blur(saturation(video,5),5)
```

<h3> Timeline </h3>

The timeline is where all the various media objects are compiled together. Once the `timeline` declaration is created, everything after is placed directly to the timeline, and the program ends when the render directive is written:

```
video v_1 = "my_cool_lets_play.mp4" ()

timeline
v_1 (0)
<media variable name> <start time> <z layer>
.
.
.
render "file.mp4" [1920,1080]
```

<h3> Example </h3>

```
video intro = "intro.mp4" (0,e) |> saturation(3) |> speed(1.5)
audio music = "music.mp3" (0,e) |> volume(2) |> noise_filter(-60)
video game_footage = "game_footage.mp4" (0,30) + (35,49)
video webcam_footage = "webcam_footage.mp4" (0,30) + (35,49) |> transform(1000,320) |> scale(0.2,0.2)

timeline
intro 0 z=1
game_footage after intro z=1
music 0 z=1
webcam_footage after intro z=2

render "lets_play.mp4" [1920,1080]
```
