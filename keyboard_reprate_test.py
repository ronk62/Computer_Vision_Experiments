# no she-bang in Windows

import time, os, keyboard

maxDeltaTime = 0.0
minDeltaTime = 999999999

countSlowReprate = 0

while True:
    prevTime = time.time()
    if keyboard.is_pressed(45):
        print("is pressed")
    deltaTime = time.time() - prevTime
    reprate = 1/(deltaTime + 0.00000001)
    if deltaTime > maxDeltaTime:
        maxDeltaTime = deltaTime
    if deltaTime < minDeltaTime:
        minDeltaTime = deltaTime
    if reprate < 600:
        print("deltaTime is ", deltaTime)
        print("reprate is ", reprate)
        print("maxDeltaTime is ", maxDeltaTime)
        print("minDeltaTime is ", minDeltaTime)
    if reprate < 600:
        countSlowReprate += 1
    if countSlowReprate > 9:
        break
    