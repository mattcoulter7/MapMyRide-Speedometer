import pyperclip
from PIL import Image, ImageDraw, ImageFont
import os
import moviepy.video.io.ImageSequenceClip
import time

class pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Print iterations progress
def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def string_to_point(str):
    str = str.split(",")
    x = float(str[0])
    y = float(str[1])
    return pt(x,y)

def get_points():
    print("Export the polyline vector from illustrator, then paste the result into here")
    pasted = ""
    while True:
        line = input()
        if line:
            pasted += line
        else:
            break
    if ("points=" in pasted):
        path = pasted.split("points=")
        path = path[1]
        path = path.split("\"")
        path = path[1]
        strPoints = path.split(" ")
        ptPoints = []
        for p in strPoints:
            if (p != ""):
                ptPoints.append(string_to_point(p))
        return ptPoints
    else:
        print("Error: The input either does not have enough points or contains curved lines.")
    return get_points()

def get_gradient(point1,point2):
    return (point2.y - point1.y)/(point2.x - point1.x)

def get_y(points,x):
    i = 0
    while (i < len(points)):
        if (x == points[i].x):
            return points[i].y
        elif (x > points[i].x):
            i += 1
        else:
            break;
    m = get_gradient(points[i],points[i-1])
    c = points[i-1].y
    return (m*(x-points[i-1].x) + c)

def get_min(points,xy):
    min = pt(None,None)
    if (xy == 'x'):
        for point in points:
            if (min.x == None or point.x < min.x):
                min = point
    elif (xy == 'y'):
        for point in points:
            if (min.y == None or point.y < min.y):
                min = point
    return min

def get_max(points,xy):
    max = pt(None,None)
    if (xy == 'x'):
        for point in points:
            if (max.x == None or point.x > max.x):
                max = point
    elif (xy == 'y'):
        for point in points:
            if (max.y == None or point.y > max.y):
                max = point
    return max

def get_step_points(points,accuracy):
    start = get_min(points,'x').x
    end = get_max(points,'x').x

    stepPoints = []
    step = (end - start) / accuracy

    curStep = start
    while (curStep < end):
        stepPoints.append(pt(curStep,get_y(points,curStep)))
        curStep += step

    return stepPoints

def get_speeds(points,maxspeed):
    min = get_min(points,'y').y
    max = get_max(points,'y').y
    speeds = []
    realMax = max - min
    for p in points:
        speed = round((1 - (p.y / realMax)) * maxspeed,2)
        speeds.append(speed)
    return speeds

def generate_images(speeds):
    print("Generating Images . . .")
    print_progress_bar(0, len(speeds), prefix = 'Progress:', suffix = 'Complete', length = 50)

    dir = "temp"
    if not os.path.exists(dir):
        os.mkdir(dir)

    i = 0
    while (i < len(speeds)):        
        img = Image.new('RGB', (400, 80), color = (35,167,0))
        fnt = ImageFont.truetype('arial.ttf', 64)
        d = ImageDraw.Draw(img)
        d.text((8,8), "{} km/h".format(speeds[i]), font=fnt, fill=(255,255,255))
        img.save('temp/{}.png'.format(i))
        i += 1
        print_progress_bar(i, len(speeds), prefix = 'Progress:', suffix = 'Complete', length = 50)

def sort_images(images):
    print("Sorting list of images . . .")
    print_progress_bar(0, len(images), prefix = 'Progress:', suffix = 'Complete', length = 50)
    startingIndex = 0
    while (startingIndex < len(images)):
        i = startingIndex + 1
        while (i < len(images)):
            img1 = int(images[startingIndex].split('/')[1].split('.')[0])
            img2 = int(images[i].split('/')[1].split('.')[0])
            if (img1 > img2):
                temp = images[startingIndex]
                images[startingIndex] = images[i]
                images[i] = temp
            i += 1
        startingIndex += 1
        print_progress_bar(startingIndex, len(images), prefix = 'Progress:', suffix = 'Complete', length = 50)
    return images

def generate_video(framerate):
    image_folder='temp'

    image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".png")]
    image_files = sort_images(image_files)
    
    print("Rendering Video . . .")
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=framerate)
    clip.write_videofile('export.mp4')

def main():
    temp = ""
    points = get_points()

    while True:
        print("How long was the trip? (seconds)")
        temp = input()
        if (temp.isdigit()):
            break
        else:
            print("Error: Please enter a valid number")
    length = int(temp)

    while True:
        print("What is the frame rate of the video? (fps)")
        temp = input()
        if (temp.isdigit()):
            break
        else:
            print("Error: Please enter a valid number")
    framerate = int(temp)

    while True:
        print("What is the max speed of the graph? (km/h)")
        temp = input()
        if (isfloat(temp)):
            break
        else:
            print("Error: Please enter a valid number")
    maxspeed = float(temp)

    accuracy = framerate*length
    stepPoints = get_step_points(points,accuracy)
    speeds = get_speeds(stepPoints,maxspeed)
    generate_images(speeds)
    generate_video(framerate)

if __name__ == "__main__":
    main()