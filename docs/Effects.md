<h1>Effects</h1>
<p>DVEL supports effects for both videos and audio. Options include:</p>
<h3>Supported Effects:</h3>
<ul>
    <li>Saturation</li>
    <li>Blur</li>
    <li>Speed</li>
    <li>Transform</li>
    <li>Location</li>
    <li>Rotation</li>
    <li>Scale</li>
    <li>Crop</li>
    <li>Volume</li>
    <li>Noise Filter</li>
</ul>

<p>Effects are declared while defining a media variable or after one is defined.</p>

<h3>Defining Effects While Declaring Media Variables:</h3>

```
video v_1 = "cool_video.mp4" (0,e) |> blur(5) |> saturation(5)
```

<h3>Defining Effects on Previously Declared Media Variables:</h3>

```
v_1 = |> blur(5) |> saturation(5)
```

<p>In either case, the effect is applied by entering the name with any values inside of parenthesis, separated by commas (if there are multiple values).</p>

<h3>Effect Details</h3>

<h4>Saturation</h4>
<p>Defines the intensity, purity, or vividness of colors within an image. It is measured as a percentage (0-100).</p>

```
saturation(x)
```
<p>Where x is equal to the saturation value.</p>

<h4>Blur</h4>
<p>Used to make an image or video clouded or smeared. It is measured as a percentage (0-100).</p>

```
blur(x)
```
<p>Where x is equal to the blur value.</p>

<h4>Speed</h4>
<p>The rate of playback, or how fast/slow a clip moves relative to its original recording speed. Expressed as a percentage of the original recording speed. Allowed values fall in range: 0.25 - 2.</p>

```
speed(x)
```
<p>Where x is equal to the speed.</p>

<h4>Transform</h4>
<p></p>

```

```

<h4>Location</h4>
<p>The anchor point of the video on the screen, expressed as (x,y) coordinates. You must also define the video resolution (width, height).</p>

```
location(x_coordinate, y_coordinate, resolution_width, resolution_height)
```

<h4>Rotation</h4>
<p>A transformation tool that changes the orientation of a clip, image, or text by spinning it around its axis. The rotation value is measured in degrees (0-360).</p>

```
rotation(x)
```
<p>Where x is equal to the degrees of rotation.</p>

<h4>Scale</h4>
<p>A transformative tool used to alter the size of a clip, image, or text element, allowing it to be increased (enlarged) or decreased (reduced) in size. It is expressed as a percentage of its original size of 100%.</p>

```
scale(x)
```
<p>Where x is equal to the percentage of scale.</p>

<h4>Crop</h4>
<p>A tool that allows the cutting away of the outer edges of a video frame to remove unwanted elements.</p>

```
crop(width, height, x_offset, y_offset)
```
<p>Where the width and height represent the width and height of the cropped video's area. And the x and y offsets represent the amount of pixels to crop from each axis.</p>

<h4>Volume</h4>
<p>A measure representing how loud or quiet a piece of audio is.</p>

```
volume(x)
```
<p>Where x is equal to the volume of the audio or video clip.</p>

<h4>Noise Filter</h4>
<p>A tool designed to reduce or eliminate unwanted constant background sounds.</p>

```
noise_filter(x)
```
<p>Where x is the noise filter value.</p>

<h3>Next: <a href="#timeline">Timeline</a></h3>