<h1>Timeline</h1>
<p>The timeline is where you arrange, trim, and layer video, audio, and effects in a chronological order. DVEL supports the following timeline declaration structure.</p>

```
timeline
intro 0 1
game_footage after intro 1
music 0 1
webcam_footage after intro z=2
```
<h3>Timeline Declaration</h3>
<p>The above code example shows that DVEL requires you to declare the start of a timeline sequence using the "timeline" keyword.</p>

<h3>Chronological Ordering</h3>
<p>Media variables are placed in chronological order. In the above example, "intro" plays first, followed by "game_footage". The audio variable "music" plays at the same time as "intro" (denoted by 0 1).</p>

<p>The "after" keyword is used to denote when the media should start. In the above example, "intro" ends at 1, and "game_footage" plays after 1.</p>

<h3>Layering</h3>
<p>The "z" parameter donotes the layer where the media should be placed. In the above example, "webcam_footage" is on layer 2, meaning it plays on top of "game_footage".</p>

<h3>Next: <a href="Commenting.md">Commenting Your Code</a></h3>