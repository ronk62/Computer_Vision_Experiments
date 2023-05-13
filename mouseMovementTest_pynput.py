# no she-bang in Windows

'''
Notes:
- pynput mouse controls work predictably in Unreal Tournament 99 (UT99, GOTY)

ref. https://pynput.readthedocs.io/en/latest/mouse.html#controlling-the-mouse

- example code from documentation below...

from pynput.mouse import Button, Controller

mouse = Controller()

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

# Set pointer position
mouse.position = (10, 20)
print('Now we have moved it to {0}'.format(
    mouse.position))

# Move pointer relative to current position
mouse.move(5, -5)

# Press and release
mouse.press(Button.left)
mouse.release(Button.left)

'''

import time
from pynput.mouse import Button, Controller

mouse = Controller()

y_distance = 0
x_distance = 30

while True:
    input("Wait at prompt ")
    for i in range(1,6):
        print(i)
        time.sleep(1)

    for i in range(1,11):
        print("move mouse right, then left, relative")
        
        print(x_distance)

        # Move pointer relative to current position
        mouse.move(x_distance, y_distance)

        # y_distance = -1 * y_distance
        x_distance = -1 * x_distance

        time.sleep(5)
        
    


