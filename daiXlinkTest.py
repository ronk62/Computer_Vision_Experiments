import numpy as np
import time
import matplotlib.pyplot as plt
import dxcam
import cv2
import depthai as dai
import keyboard

camera = dxcam.create(device_idx=0, output_idx=1)  # returns a DXCamera instance on primary monitor

#####

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
xinFrame = pipeline.create(dai.node.XLinkIn)
xoutFrame = pipeline.create(dai.node.XLinkOut)

xinFrame.setStreamName("inFrame")
xoutFrame.setStreamName("outFrame")


# Linking
xinFrame.out.link(xoutFrame.input)

#####

# Connect and start the pipeline
with dai.Device(pipeline) as device:

    print(device.getUsbSpeed())

    q_inFrame = device.getInputQueue(name="inFrame", maxSize=1, blocking=True)
    q_outFrame = device.getOutputQueue(name="outFrame", maxSize=1, blocking=True)

    # init vars and np arrays
    count = 0

    countArray = np.array([], dtype=np.int8)      # array to hold indepenant var "count"
    dtCaparray = np.array([], dtype=np.float32)     # array to hold screen Cap delta time
    dtXlinkSendarray = np.array([], dtype=np.float32)    # array to hold Xlink Send delta time
    dtXlinkRcvarray = np.array([], dtype=np.float32)    # array to hold Xlink Rcv delta time
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


    def to_planar(arr: np.ndarray, shape: tuple) -> np.ndarray:
        return cv2.resize(arr, shape).transpose(2, 0, 1).flatten()

    baseTs = time.monotonic()
    simulatedFps = 30
    # inputFrameShape = (1920, 1080)
    inputFrameShape = (1600, 900)


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

        #####

        if activeFrame.size < 2:
            continue

        activeFrame = cv2.cvtColor(activeFrame, cv2.COLOR_RGB2BGR)

        img = dai.ImgFrame()
        img.setType(dai.ImgFrame.Type.BGR888p)
        img.setData(to_planar(activeFrame, inputFrameShape))
        img.setTimestamp(baseTs)
        baseTs += 1/simulatedFps

        img.setWidth(inputFrameShape[0])
        img.setHeight(inputFrameShape[1])
        q_inFrame.send(img)
        dtXlinkSend, previous_time = deltaT(previous_time)

        xlinkRetFrame = q_outFrame.tryGet()
        dtXlinkRcv, previous_time = deltaT(previous_time)

        #####

        if activeFrame.size > 1:
            displayFrame("activeFrame", activeFrame)

            if cv2.waitKey(1) == ord('q'):
                break

        dtShow, previous_time = deltaT(previous_time)
        dtLoop, previous_time = deltaT(initTime)

        ## update arrays
        countArray = np.append(countArray, count)
        dtCaparray = np.append(dtCaparray, dtCap)
        dtXlinkSendarray = np.append(dtXlinkSendarray, dtXlinkSend)
        dtXlinkRcvarray = np.append(dtXlinkRcvarray, dtXlinkRcv)
        dtShowarray = np.append(dtShowarray, dtShow)
        dtLoopArray = np.append(dtLoopArray, dtLoop)

        print("")
        print('dtCap = {}, dtXlinkSend = {}, dtXlinkRcv = {}, dtShow = {}, dtLoop = {}'.format(dtCap, dtXlinkSend, dtXlinkRcv, dtShow, dtLoop))

        # time.sleep(0.001)

# compute stats
dtCapMin = np.min(dtCaparray)
dtCapMax = np.max(dtCaparray)
dtCapAvg = np.average(dtCaparray)
dtCapStd = np.std(dtCaparray)

dtXlinkSendMin = np.min(dtXlinkSendarray)
dtXlinkSendMax = np.max(dtXlinkSendarray)
dtXlinkSendAvg = np.average(dtXlinkSendarray)
dtXlinkSendStd = np.std(dtXlinkSendarray)

dtXlinkRcvMin = np.min(dtXlinkRcvarray)
dtXlinkRcvMax = np.max(dtXlinkRcvarray)
dtXlinkRcvAvg = np.average(dtXlinkRcvarray)
dtXlinkRcvStd = np.std(dtXlinkRcvarray)

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
print("")
print('dtXlinkSendMin = {}, dtXlinkSendMax = {}, dtXlinkSendAvg = {}, dtXlinkSendStd = {}'.format(dtXlinkSendMin, dtXlinkSendMax, dtXlinkSendAvg, dtXlinkSendStd))
print("")
print('dtXlinkRcvMin = {}, dtXlinkRcvMax = {}, dtXlinkRcvAvg = {}, dtXlinkRcvStd = {}'.format(dtXlinkRcvMin, dtXlinkRcvMax, dtXlinkRcvAvg, dtXlinkRcvStd))
print("")
print('dtShowMin = {}, dtShowMax = {}, dtShowAvg = {}, dtShowStd = {}'.format(dtShowMin, dtShowMax, dtShowAvg, dtShowStd))
print("")
print('dtLoopMin = {}, dtLoopMax = {}, dtLoopAvg = {}, dtLoopStd = {}'.format(dtLoopMin, dtLoopMax, dtLoopAvg, dtLoopStd))

### plot the data, then exit
## Create plots
plt.figure(1)
plt.plot(countArray,dtCaparray, label='dtCaparray')
plt.plot(countArray,dtXlinkSendarray, label='dtXlinkSendarray')
plt.plot(countArray,dtXlinkRcvarray, label='dtXlinkRcvarray')
plt.plot(countArray,dtShowarray, label='dtShowarray')
plt.plot(countArray,dtLoopArray, label='dtLoopArray')
plt.legend()
plt.show()

print("exiting...")
exit()