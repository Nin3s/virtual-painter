# Overview
A painting app created by using OpenCV and Python that allows a user to draw on the air with their webcamera. The goal was for me to set up OpenCV for future projects.


I created this application following a tutorial which is linked [here.](https://analyticsindiamag.com/how-to-create-a-virtual-painting-app-using-opencv/) One of the changes I made was adding the ability to modify what color the tracker should look out for. Using the default value from the website made it difficult for my camera to pick up the right colors, so I needed an easy way to modify it without having to directly hard code it.

## Requirements
1. Python
2. OpenCV
3. NumPy

Note: I had difficulty getting OpenCV to run in WSL, but it worked fine for me once I switched to Windows. In WSL, the window pops up but immediately closes down. It might've been a file path issue for the camera, but I wasn't too sure.

## RGB vs BGR vs HSV (Because it confused me too) And Setting Tracker Color
HSV stands for Hue, Saturation, and Value. In the tracker modifier, there's an upper value and a lower value to set it. By default, lower is set to 0 and upper to 255. It might take some time to get the color of your tracker right, but it should work afterwords. Make sure you don't have any similar colors in your background or the paint may jump around. Keep in mind the lighting of the room as well. [Here's a nifty document about colorspaces in OpenCV](https://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html)

![image](https://user-images.githubusercontent.com/50024330/204200760-624c8d0e-187d-4f33-a760-627c642bcec1.png)

BGR is a reversed arrangement of pixels from RGB. Apparently the reason why OpenCV uses it is because of [historial reasons](https://stackoverflow.com/questions/14556545/why-opencv-using-bgr-colour-space-instead-of-rgb)

## What I Learned
1. Setting up and using OpenCV
2. Create/Capture camera output
3. Creating a window for various things like the aforementioned camera output and the HSV modifiers
