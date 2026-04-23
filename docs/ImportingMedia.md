<h1>Importing Media</h1>
<p>DVEL supports the following media types:</p>
<ul>
    <li>Videos (.mp4, .mov, .avi, and most other modern and legacy formats.)</li>
    <li>Images (.jpeg, .png, .gif, and more other standard and professional image formats.)</li>
    <li>Audio (.mp3, .wav, and most other audio formats.)</li>
</ul>

<h3>Use the following format to import media</h3>

```
<type> <name> = <filepath> <duration> <effects>
```

<h3>Examples</h3>

```
video intro = "intro.mp4" (0,e) |> saturation(3) |> speed(1.5)
audio music = "music.mp3" (0,e) |> volume(2) |> noise_filter(-60)
image logo = "logo.png" (0,e)
```

<h3>Next: <a href="Operations.md">Operations</a></h3>