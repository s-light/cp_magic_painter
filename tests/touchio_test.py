import time
import board
import touchio

print("")
print("touchio_test.py")

touch_pin1 = touchio.TouchIn(board.D5)
touch_pin2 = touchio.TouchIn(board.D6)

touch_pin1.threshold = touch_pin1.raw_value + 3000
touch_pin2.threshold = touch_pin2.raw_value + 3000

while True:
    print(
        "{:>5} - {:>7}"
        "     "
        "{:>5} - {:>7}"
        "".format(
            touch_pin1.value,
            touch_pin1.raw_value,
            touch_pin2.value,
            touch_pin2.raw_value,
        )
    )
    time.sleep(0.2)
