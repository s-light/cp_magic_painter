# based on example
# https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH/blob/main/examples/lis3dh_simpletest.py
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board

import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT



def speed_test(fn, msg, count=1000):
    print("{} speed test running..".format(msg))
    start = time.monotonic()
    for i in range(count):
        fn()
    end = time.monotonic()
    duration = (end - start) / count
    duration_ms = duration * 1000
    result = {
        "msg": msg,
        "duration_ms": duration_ms,
    }
    print(
        "'{}'  needs {:10.3f}ms/call".format(
            result["msg"],
            result["duration_ms"],
        )
    )
    return result


def print_results(speed_tests):
    msg_max_length = max(len(x["msg"]) for x in speed_tests)
    # print(msg_max_length)
    for test in speed_tests:
        msg_template = (
            "'{:<" + "{}".format(msg_max_length + 5) + "}'  needs {:10.4f}ms/call"
        )
        print(
            msg_template.format(
                test["msg"],
                test["duration_ms"],
            )
        )


print("\n" * 20)
speed_tests = []


if hasattr(board, "DISPLAY"):
    import displayio
    print("deactivate display..")
    board.DISPLAY.auto_refresh = False
    board.DISPLAY.root_group = displayio.Group()



def toggle_led():
    led.value = not led.value

speed_tests.append(
    speed_test(
        toggle_led,
        msg="toggle_led",
        count=100000,
    )
)

def toggle_led2():
    led.value = True
    led.value = False

speed_tests.append(
    speed_test(
        toggle_led2,
        msg="toggle_led2",
        count=100000,
    )
)







if hasattr(board, "DISPLAY"):
    print("activate display..")
    board.DISPLAY.auto_refresh = True
    board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL





print("\n" * 20)
time.sleep(1)

print_results(speed_tests)
time.sleep(1)

print("done...")
