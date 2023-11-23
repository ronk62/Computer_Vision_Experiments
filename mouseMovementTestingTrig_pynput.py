# no she-bang in Windows

import time
import keyboard
import math
import numpy as np
from pynput.mouse import Button, Controller
import matplotlib.pyplot as plt


# init vars
targetY = 450
targetX = 1

# init np arrays
timestampArray = np.array([], dtype=np.float32)       # array to hold timestamps
targetYarray = np.array([], dtype=np.float32)         # array to hold raw screen targetY
mouseMotionYarray = np.array([], dtype=np.float32)    # array to hold mouseMotionY

targetXarray = np.array([], dtype=np.float32)         # array to hold raw screen targetX
mouseMotionXarray = np.array([], dtype=np.float32)    # array to hold mouseMotionX


mouse = Controller()

'''
ref. https://pynput.readthedocs.io/en/latest/mouse.html#controlling-the-mouse
ref. https://www.unknowncheats.me/forum/apex-legends/495561-calculate-mouse-movement-value.html
'''
gameScrnWidth = 1600
gameScrnHeight = 900
UT99FOV = 90
UT99sens = 1
UTfull360 = 16363.0 / UT99sens


# def click():
#     # Press and release
#     mouse.press(Button.left)
#     mouse.release(Button.left)


def RealFov(fov, width, height):
    raspectRatio = (width / height) / (4/3)
    rFovRad = 2 * math.atan(math.tan(math.radians(fov * 0.5)) * raspectRatio)
    rFovDeg = math.degrees(rFovRad)
    return rFovDeg

def coord2deg (delta, fov, width):
    coordRad = math.atan(((delta * 2) / width) * math.tan(math.radians(fov * 0.5)))
    coordDeg = math.degrees(coordRad)
    return coordDeg

'''
ref.
gameScrnWidth = 1600
gameScrnHeight = 900
UT99FOV = 90
UT99sens = 1
UTfull360 = 16363.0 / UT99sens
'''
def AimMouseAlt(target):
    offsetY, offsetX = target

    realUT99fov = RealFov(UT99FOV, gameScrnWidth, gameScrnHeight)

    yaw = coord2deg(offsetX - gameScrnWidth / 2, realUT99fov, gameScrnWidth)
    pitch = coord2deg(offsetY - gameScrnHeight / 2, realUT99fov, gameScrnWidth)

    y_distance = int((pitch * 1))
    x_distance = int((yaw * 1))

    # print("y_distance, x_distance ", y_distance, x_distance)
    # Move pointer relative to current position
    # mouse.move(x_distance, y_distance)
    return x_distance, y_distance


def plotTheData():
    ## Create plot(s)

    # raw-target values
    plt.figure(1)
    plt.plot(timestampArray,targetYarray, label='targetYarray')
    plt.plot(timestampArray,targetXarray, label='targetXarray')

    # mouseMotion values
    plt.plot(timestampArray,mouseMotionYarray, label='mouseMotionYarray')
    plt.plot(timestampArray,mouseMotionXarray, label='mouseMotionXarray')

    plt.xlabel('dT')
    plt.ylabel('raw-target and error values')
    plt.title('target and mouseMotion values over time')
    plt.legend()
    plt.show()

    print("exiting...")
    exit()


### main ###

## do one of the following...

#create Targ Data Incr TargetX
for i in range(1,1601):
    targetY = 450
    targetX = i
    targ = (targetY, targetX)

    mouseMotionX, mouseMotionY = AimMouseAlt(targ)
    print("targetY, mouseMotionY, targetX, mouseMotionX ", targetY, mouseMotionY, targetX, mouseMotionX)

    ## Update arrays
    currentTime = time.time()
    timestampArray = np.append(timestampArray, currentTime)
    targetYarray = np.append(targetYarray, targetY)
    targetXarray = np.append(targetXarray, targetX)
    mouseMotionYarray = np.append(mouseMotionYarray, mouseMotionY)
    mouseMotionXarray = np.append(mouseMotionXarray, mouseMotionX)


# #create Targ Data Incr TargetY
# for i in range(1,901):
#     targetY = i
#     targetX = 800
#     targ = (targetY, targetX)

#     mouseMotionX, mouseMotionY = AimMouseAlt(targ)
#     print("targetY, mouseMotionY, targetX, mouseMotionX ", targetY, mouseMotionY, targetX, mouseMotionX)

#     ## Update arrays
#     currentTime = time.time()
#     timestampArray = np.append(timestampArray, currentTime)
#     targetYarray = np.append(targetYarray, targetY)
#     targetXarray = np.append(targetXarray, targetX)
#     mouseMotionYarray = np.append(mouseMotionYarray, mouseMotionY)
#     mouseMotionXarray = np.append(mouseMotionXarray, mouseMotionX)

# plot results...
plotTheData()
