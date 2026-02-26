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
 
> The following is not the syntax we will want to use for this project but serves as an example of functionality using a Pythonic style.
  
```
import tutorial_video from 'video.mp4'
import intro from 'intro.mp4'
import watermark from 'watermark.png

tutorial_video = intro + tutorial_video # the tutorial video is appended after the intro
watermark.scale(0.1,0.1, center) # scales the x and y coordinates of the watermark image to 10%, treating the center of the image as the origin. 
watermark.align(bottom-right)
tutorial_video.overlay(watermark)
tutorial_video.volume = tutorial_video.volume - 2 # if video is too loud, control the dB value.


export(tutorial_video, tutorial/final.mp4)
```
The final result will be their tutorial video, with a watermark in the bottom right, with the intro at the beginning of the video and slightly quieter volume.

Potentially we may with to splice videos, perhaps to remove dead space:
```
tutorial_video = tutorial_video[0:04.43...tutorial_video.length-0:05] # Removes the first 4 seconds and last 5 seconds of tutorial_video
```

<h3> Current Goals </h3>

<ul>
  <li> Develop declarative style syntax that makes video editing as simple as possible. </li>
  <li> Determine the scope of the project: How much we will commit to finishing by the end of the course? </li>
  <li> Develop tentative software architecture: Answers the question how we will organize our code? </li>
</ul>
We will will individual research and document our findings but collectively come to final decisions on each of the topics during our in-person meeting times. 

</p>
