import time
import board
import touchio

import touchio

# wait a little till the computer / serial-terminal is ready...
time.sleep(1)
print("")
print("touchio_minimal_test.py")

touch_pin = touchio.TouchIn(board.D5)

print("print touch_pin value in an endless loop:")
while True:
    print(touch_pin.value)
    time.sleep(0.1)