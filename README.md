# MapMyRide-Speedometer
https://youtu.be/syajaB8xJ7k Generate a Speedomoter overlay for your video from a speed graphover time graph!

## Dependencies
- moviepy
- PIL

## How to use
1. Screenshot the Speed over Time graph from MapMyRide
2. Open the image in Adobe Illustrator, and use the pen tool and trace over the speed line. (Only use linear lines!)
3. Select the lines and press ctrl + c, this will copy the point information into your clipboard
4. Run `python main.py`, then paste your clipboard into terminal
5. Specify:
    1. How long was the trip? (seconds)
    2. What is the frame rate of the video? (fps)
    3. What is the max speed of the graph? (km/h)
6. The video will be rendered, and exported to the app folder directory

## Example
1. Screenshot\
![image](https://user-images.githubusercontent.com/53892067/199867933-97ee9664-3a44-4afa-a0c7-9b36da8ce98e.png)
2. Trace\
![image](https://user-images.githubusercontent.com/53892067/199867964-49ea6c2a-16bb-4856-b7c6-2b84965b5cf3.png)
3. Trace Data\
![image](https://user-images.githubusercontent.com/53892067/199868051-86dd6a45-d259-42c6-8241-484016d8e587.png)
4. Output\
![image](https://user-images.githubusercontent.com/53892067/199868119-533e6ff9-8c3e-4d92-b908-c27acdc699e9.png)
