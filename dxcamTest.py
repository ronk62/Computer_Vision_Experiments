import numpy as np
import time
import matplotlib.pyplot as plt
import dxcam
import cv2
import keyboard


camera = dxcam.create(device_idx=0, output_idx=1)  # returns a DXCamera instance on primary monitor


# init vars and np arrays
count = 0

countArray = np.array([], dtype=np.int8)      # array to hold indepenant var "count"
dtCaparray = np.array([], dtype=np.float32)     # array to hold screen Cap delta time
dtShowarray = np.array([], dtype=np.float32)    # array to hold image Show delta time
dtLoopArray = np.array([], dtype=np.float32)    # array to hold full Loop delta time

def displayFrame(name, frame):
    cv2.imshow(name, frame)
  

def capture_window_dxcam():
    # UT game in 1278 x 686 windowed mode
    image = np.array(camera.grab([0, 0, 1600, 900]))
    return image


def deltaT(previous_time):
    dt = time.time() - previous_time
    previous_time = time.time()
    return dt, previous_time


while True:
    if keyboard.is_pressed(46):     # press and hold 'c' to exit
            print("breaking loop; plotting data...")
            break
    
    count += 1
    previous_time = time.time()
    initTime = previous_time
    dtLoop, previous_time = deltaT(previous_time)
    activeFrame = capture_window_dxcam()
    dtCap, previous_time = deltaT(previous_time)

    if activeFrame.size > 1:
        displayFrame("activeFrame", activeFrame)

        if cv2.waitKey(1) == ord('q'):
            break

    dtShow, previous_time = deltaT(previous_time)
    dtLoop, previous_time = deltaT(initTime)

    ## update arrays
    countArray = np.append(countArray, count)
    dtCaparray = np.append(dtCaparray, dtCap)
    dtShowarray = np.append(dtShowarray, dtShow)
    dtLoopArray = np.append(dtLoopArray, dtLoop)

    print("")
    print('dtCap = {}, dtShow = {}, dtLoop = {}'.format(dtCap, dtShow, dtLoop))

    # time.sleep(0.001)

# compute stats
dtCapMin = np.min(dtCaparray)
dtCapMax = np.max(dtCaparray)
dtCapAvg = np.average(dtCaparray)
dtCapStd = np.std(dtCaparray)

dtShowMin = np.min(dtShowarray)
dtShowMax = np.max(dtShowarray)
dtShowAvg = np.average(dtShowarray)
dtShowStd = np.std(dtShowarray)

dtLoopMin = np.min(dtLoopArray)
dtLoopMax = np.max(dtLoopArray)
dtLoopAvg = np.average(dtLoopArray)
dtLoopStd = np.std(dtLoopArray)

# print stats
print("")
print("")
print('dtCapMin = {}, dtCapMax = {}, dtCapAvg = {}, dtCapStd = {}'.format(dtCapMin, dtCapMax, dtCapAvg, dtCapStd))
print('dtShowMin = {}, dtShowMax = {}, dtShowAvg = {}, dtShowStd = {}'.format(dtShowMin, dtShowMax, dtShowAvg, dtShowStd))
print('dtLoopMin = {}, dtLoopMax = {}, dtLoopAvg = {}, dtLoopStd = {}'.format(dtLoopMin, dtLoopMax, dtLoopAvg, dtLoopStd))

### plot the data, then exit
## Create plots
plt.figure(1)
plt.plot(countArray,dtCaparray, label='dtCaparray')
plt.plot(countArray,dtShowarray, label='dtShowarray')
plt.plot(countArray,dtLoopArray, label='dtLoopArray')
plt.legend()
plt.show()

print("exiting...")
exit()