# no she-bang in Windows

from Keyboard_And_Mouse_Controls import *
import math

y_distance = 0
x_distance = 30

while True:
    input("Wait at prompt ")
    for i in range(1,6):
        print(i)
        time.sleep(1)


    print("move mouse ")
    for i in range(1,27):
        print(i, x_distance)
        # x_distance = -i
        
        # y_distance = -1 * y_distance
        x_distance = -1 * x_distance
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0)

        win32api.SetCursorPos((0,0))

        time.sleep(1)

    


