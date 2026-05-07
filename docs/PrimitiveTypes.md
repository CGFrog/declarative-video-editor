<h1>Primitive Types</h1>
<p>DVEL supports the following primitive types:</p>
<ul>
    <li>Integer: Declared by using the 'num' text before the variable name of your choice.</li>
    <li>String: Declared by using the 'str' text before the variable name of your choice.</li>
</ul>

<h3>Primitive Types Examples</h3>

```
num smoke = 5
video lecture_video = "lecture_video.mp4" (0, e) |> blur(smoke);

str color = "0x00FF00" (Hex color for Green)
video lecture_video = "lecture_video.mp4: (0, e) |> chromakey(color, 0.5, 0.5);
```

<p>The code snippets above define a video called "lecture_video" which seperately inputs a blur effect into the "lecture_video.mp4" of the smoke variable value which is 5. It also defines another "lecture_video" which defines a string that is the hexcolor of green. This string is then used in the chromakey function to pick the color that you want to make transparent.</p>

<h3>Next: <a href="Operations.md">Operations</a></h3>