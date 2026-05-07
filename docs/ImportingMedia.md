<h1>Importing Media</h1>
<h2>Main Media Types</h2>
<p>DVEL supports the following media types:</p>
<ul>
    <li>Videos (.mp4, .mov, .avi, and most other modern and legacy formats.)</li>
    <li>Images (.jpeg, .png, .gif, and most other standard and professional image formats.)</li>
    <li>Audio (.mp3, .wav, and most other audio formats.)</li>
</ul>

<h3>Use the following format to import media</h3>
<p>Pro tip: Don't forget the semicolon after each declaration line! DVEL supports multi-line declarations!</p>

```
<type> <name> = <filepath> <duration> <effects>;
```

<h3>Examples</h3>

```
video intro = "intro.mp4" (0,e)
    |> saturation(3) 
    |> speed(1.5);
audio music = "music.mp3" (0,e)|> volume(2);
image logo = "logo.png" (0,e);
```

<h2>Other Types</h2>
<p>DVEL supports the following declarations as well:</p>
<ul>
    <li>Captions (simple text placed at the bottom-center of the screen)</li>
</ul>

<h3>Examples</h3>

```
str text1 = "Hello World.";
caption caption1 = "This is a caption." 4;
```
<p>In the above example, the 4 represents the caption being displayed for 4 seconds.</p>

```
str caption_text = "Here is text for my caption.";
caption caption_display = caption_text 4;
```
<p>The above example shows a string and caption being declared separately, with the string assigned to the captions value. The caption's duration is 4 seconds.</p>

<h3>Next: <a href="PrimitiveTypes.md">Primitive Types</a></h3>
