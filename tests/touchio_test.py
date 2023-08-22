import time
import board
import touchio

print("")
print("touchio_test.py")

touch_pin1 = touchio.TouchIn(board.D5)
touch_pin2 = touchio.TouchIn(board.D6)
touch_pin3 = touchio.TouchIn(board.D7)

print(
        "{:>5} - {:>7}"
        "     "
        "{:>5} - {:>7}"
        "     "
        "{:>5} - {:>7}"
        "".format(
            touch_pin1.value,
            touch_pin1.raw_value,
            touch_pin2.value,
            touch_pin2.raw_value,
            touch_pin3.value,
            touch_pin3.raw_value,
        )
    )

touch_pin1.threshold = touch_pin1.raw_value + 4000
touch_pin2.threshold = touch_pin2.raw_value + 4000
touch_pin3.threshold = touch_pin3.raw_value + 4000

while True:
    print(
        "{:>5} - {:>7}"
        "     "
        "{:>5} - {:>7}"
        "     "
        "{:>5} - {:>7}"
        "".format(
            touch_pin1.value,
            touch_pin1.raw_value,
            touch_pin2.value,
            touch_pin2.raw_value,
            touch_pin3.value,
            touch_pin3.raw_value,
        )
    )
    time.sleep(0.2)
