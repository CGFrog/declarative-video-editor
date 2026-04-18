<h1>Operations</h1>
<p>DVEL supports the following operations:</p>
<ul>
    <li>Union ( + ): Concatenating two peices of media together.</li>
    <li>Function Composition ( |> ): Used when putting multiple effects on a piece of media.</li>
    <li>Timestamp ( start_time, end_time ): Used to define start and end times for videos.</li>
</ul>

<h3>Union & Timestamp Example</h3>

```
video game_footage = "game_footage.mp4" (0,30) + (35,49)
```
<p>The above code snippet defines a video called "game_footage" which is a concatenation from 0:00-0:30 seconds and 00:35-00:49 seconds from "game_footage.mp4".</p>

<h3>Function Composition</h3>

```
audio music = "music.mp3" (0,e) |> volume(2) |> noise_filter(-60)
```
<p>In order to apply multiple effects onto a single piece of media, you can use |> between each effect rule you apply (see code above).</p>

<h3>Next: <a href="Effects.md">Effects</a></h3>