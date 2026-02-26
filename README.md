<h1>
  Declarative Video Editor Language
</h1>
<p>
The goal of this project is to create a "Markup" style language that specializes in video editing. This language is not intended for use by artists but rather for fields where videos are edited to meet a repeatable, objective design standard. An online course may need an introductory slide before each video. Instead of repeatedly making the same edit to different video files, we can design a script that will make the same consistent video structure.

There are several clear advantages of this methodology:
<ul>
  <li> Source control for their video editing </li>
  <li> Allows the user to design modular components  </li>
  <li> Easily repeat tasks consistently across multiple files </li>
  <li> Edit large amounts of videos in a signle batch </li>
</ul>
<h3>Example</h3>
Let's say a user wishes to add an intro and a watermark to all of their videos. Our language will conceptually do the following:
 
> The following is not the syntax we will want to use for this project but serves as an example of functionality.
  
```
import tutorial_video from 'video.mp4'
import intro from 'intro.mp4'
import watermark from 'watermark.png

tutorial_video = intro + tutorial_video 
watermark.scale(0.1,0.1, center) # scales the x and y coordinates of the watermark image to 10%, treating the center of the image as the origin. 
watermark.align(bottom-right)
tutorial_video.overlay(watermark)

export(tutorial_video, tutorial/final.mp4)
```
</p>
