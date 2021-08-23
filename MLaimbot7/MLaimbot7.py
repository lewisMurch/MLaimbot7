#This aimbot is trained for a specific overatch character in the training area
#This aimbot is not intended for anything other than demonstration of the ability of the yolov AI model

#import needed moudules 
import cv2
import torch
import cmd
import numpy as np
from PIL import Image
import win32api, win32con, win32gui
import time
import keyboard
import pyautogui
from IPython.display import Image
import os
import sys
location = os.path.dirname(os.path.abspath(__file__))

def findModel():
    lengthOfdesiredPath = len(str(location)) - 19 #This removes 19 characters of the location of the python files location, leading it back to the main file
    modelLocation = str(location[0:lengthOfdesiredPath] + "yolov5") #creates a variable with the value of the model location path
    return(modelLocation)

def findWeight():
    lengthOfdesiredPath = len(str(location)) - 19 #This removes 19 characters of the location of the python files location, leading it back to the main file
    weightLocation = str(location[0:lengthOfdesiredPath] + "MLaimbot7CustomWeight") #creates a variable with the value of the weight location path
    return(weightLocation)


model = torch.hub.load(findModel(), 'custom', path=findWeight(), source='local') #Load the model from local storage

region = 624, 264, 672, 672 #set the region of the screen capture: left, top, width, height
confidence = 0.5 #sets the confidence level of the detection

def aim():
    img1 = np.array(pyautogui.screenshot(region = region)) #capture an image within the given region
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) #make the image greyscale

    results = model(img1, size=672) #feed the results into the model

    for i in range(0, len(results.pandas().xyxy[0])): #for each detected object in the screenshot
        if results.pandas().xyxy[0].name[i] == 'person' and results.pandas().xyxy[0].confidence[i] >= confidence: #if the program is as or above the set confidence level
            print('person found!') #for debug

            #Gets boxes coordinates and finds a midpoint, assining the midpoint to variables
            x = int(results.pandas().xyxy[0].xmax[i]) + int(results.pandas().xyxy[0].xmin[i]) 
            y = int(results.pandas().xyxy[0].ymax[i]) + int(results.pandas().xyxy[0].ymin[i])
            xUse = int(x/2)
            yUse = int(y/2)
            
            #finds the distance the mouse needs to move to get to the centre of the box
            moveMouseByx = win32api.GetCursorPos()[0] - xUse
            moveMouseByy = win32api.GetCursorPos()[1] - yUse

            #calculcates roughly where a players head will be in relation to the bounding box size
            height = results.pandas().xyxy[0].ymax[i] - results.pandas().xyxy[0].ymin[i]
            head = int(11.5 * height / 32)

            #moves the mouse to the centre of the bounding box (with an increase in vetical height to hit roughly where the head will be)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -moveMouseByx + 624,  ((-moveMouseByy) + 264 - head), 0, 0)

            #click the left mouse button
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
          
#Run the function when e is pressed
keyboard.add_hotkey('e', aim)
keyboard.wait()
