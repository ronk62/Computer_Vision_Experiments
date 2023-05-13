# no she-bang in Windows

'''
Notes:
- win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0) is
  inconsistent with movement scale from one execution to another
  - going right 100 times with x_distance = 1 does not always result in same location,
    event when start location is the same

    for j in range(1,101):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0)

- going right 30 (x_distance = 30), then left 30 (x_distance = -30) caused unpredicted
    results - not returning to orig position

- GetCursorPos() and SetCursorPos(origxy) don't actually move the mouse in UT99;
  only the cursor is relocated, but the mouse pointer (aim location)

    origxy = win32api.GetCursorPos()
    win32api.SetCursorPos(origxy)

'''

from Keyboard_And_Mouse_Controls import *
import math

y_distance = 0
x_targ_distance = 99   # total x dist goal
x_distance = 3          # distance per increment

while True:
    input("Wait at prompt ")
    for i in range(1,6):
        print(i)
        time.sleep(1)

    for i in range(1,9):
        ####
        # print("move mouse increment right")
        # x_distance = 50
        # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0)

        for j in range(1,34):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0)

        print(x_distance)

        # y_distance = -1 * y_distance
        x_distance = -1 * x_distance

        time.sleep(5)
        
    # print("move mouse increment left")
    # x_distance = -50
    # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0)

    # for i in range(1,21):
    #     print(i, x_distance)
    #     win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0)
    #     # y_distance = -1 * y_distance
    #     # x_distance = -1 * x_distance
    #     time.sleep(1)

    # time.sleep(8)
    


