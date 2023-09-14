# SPDX-FileCopyrightText: 2023 s-light.eu Stefan Krüger
# SPDX-License-Identifier: MIT


# add src as import path
import sys

sys.path.append("/src")

import time
import usb_cdc
import board
import busio
import digitalio
import displayio

import adafruit_lis3dh
from adafruit_debouncer import Button
import keypad

from user_input import UserInput

from rainbowio import colorwheel
import adafruit_dotstar

from filter.median import MedianFilter

plot_data = True

pixel_count = 36
pixels = adafruit_dotstar.DotStar(
    board.SCK,
    board.MOSI,
    pixel_count,
    brightness=1,
    auto_write=False,
)


i2c = busio.I2C(
    scl=board.SCL1,
    sda=board.SDA1,
    frequency=400000,
)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# RANGE_2_G
# RANGE_4_G
# RANGE_8_G
# RANGE_16_G
lis3dh.range = adafruit_lis3dh.RANGE_16_G

# default → 2,5ms update rate
# lis3dh.data_rate = adafruit_lis3dh.DATARATE_400_HZ
lis3dh.data_rate = adafruit_lis3dh.DATARATE_LOWPOWER_5KHZ  # → 0,2ms


filter_count = 4
filter_center = filter_count//2 -1
filter_buffer = [0] * filter_count

print("filter_buffer", filter_buffer)

# time; delta; direction_raw; y; y_filtered
# out_template = (
#     "{:10.3f}; {:10.3f}; {: 1d}; {:10.3f}; {:10.3f};    "
#     "[{:7.3f}, {:7.3f}, {:7.3f}, {:7.3f}, {:7.3f}]"
# )
out_template = (
    "{:7.3f}; {:7.3f}; {: 1d}; {:7.3f}; {:7.3f};    "
    "{:7.3f};"
    # "avg1:{:7.3f} avg2:{:7.3f};     "
    # "["
    # + ("{:7.3f}, " * filter_count)
    # + "]    "
)

y_last = 0
y_filtered = 0
noise = 1.0
direction_raw = 0
direction_raw_last = 0
direction_changed = False
# direction_filtered = 0
# direction_filtered_last = 0

# MedianFilter


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# helper

def average(input_list):
    return sum(input_list) / len(input_list)

def median_average(input_list, window_size=0.5):
    sorted_list = input_list.sort()
    window_size_el_count = len(sorted_list) * window_size
    window_start = window_size_el_count
    window_end = len(sorted_list) - window_size_el_count
    return average(sorted_list[window_start:window_end])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ui handling


def button_pushed():
    print("button pushed.")


def handle_touch(touch_id, touch):
    if touch.fell:
        if touch_id == 0:
            global plot_data
            plot_data = not plot_data
            print("\n" * 10)
            print("toggle plot_data", plot_data)
            print("\n" * 10)
        elif touch_id == 1:
            # reset
            pixels[pixel_count - 1] = (1, 0, 0)
            pixels[pixel_count // 2] = (1, 1, 0)
            pixels.show()
            for x in range(1000):
                print(out_template.format(0, 0, 0, 0, 0, 0))
            y_last = 0
            y_filtered = 0
            direction_raw = 0
            pixels.fill((0, 0, 0))
            pixels.show()
            last = time.monotonic()
            start = time.monotonic()
        elif touch_id == 2:
            print("handle_touch", touch_id)


ui_config = {
    "hw": {
        "touch": {
            "pins": [
                board.D5,
                board.D6,
                board.D7,
            ],
            "threshold": 4000,
        },
    },
}
userinput = UserInput(
    config=ui_config, callback_button=button_pushed, callback_touch=handle_touch
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# main

if hasattr(board, "DISPLAY"):
    board.DISPLAY.brightness = 0.1
    print("deactivate display..")
    board.DISPLAY.auto_refresh = False
    board.DISPLAY.root_group = displayio.Group()

start = time.monotonic()
last = time.monotonic()
try:
    while True:
        # print single accelerometer value (in m / s ^ 2).
        # print("{:10.3f}".format(lis3dh.acceleration[1])),
        # print(lis3dh.acceleration[1])
        # usb_cdc.console.write(bytes(int(lis3dh.acceleration[1]*10)))

        # Divide them by 9.806 to convert to Gs.
        y = lis3dh.acceleration[1] / adafruit_lis3dh.STANDARD_GRAVITY

        # remove oldest value
        filter_buffer.pop(0)
        # add new
        filter_buffer.append(y)

        avg1 = average(filter_buffer[:filter_center])
        avg2 = average(filter_buffer[filter_center:])

        if (
            y < (noise*-1) 
            or y > noise
        ):
            if (avg1) < avg2:
                direction_raw = +1
            elif (avg1) > avg2:
                direction_raw = -1
            else:
                direction_raw = 0

            if (
                direction_raw_last is not direction_raw 
                and direction_raw is not 0
            ):
                direction_raw_last = direction_raw
                # event! we change
                direction_changed = True
                pixels[-1] = (5, 0, 5)
            else:
                direction_changed = False
                pixels[-1] = (0, 0, 0)

            # led test output
            if direction_raw is 1:
                pixels[-3] = (0, 0, 10)
                pixels[-5] = (0, 0, 0)
                pixels[-10] = (0, 0, 0)
            elif direction_raw is -1:
                pixels[-3] = (0, 0, 0)
                pixels[-5] = (0, 10, 0)
                pixels[-10] = (0, 0, 0)
            else:
                pixels[-3] = (0, 0, 0)
                pixels[-5] = (0, 0, 0)
                pixels[-10] = (1, 0, 0)
        else:
            pixels.fill((0,0,0))
        pixels.show()

        if plot_data:
            print(
                out_template.format(
                    time.monotonic() - start,
                    (time.monotonic() - last) * 1000,
                    direction_raw,
                    y,
                    y_filtered,
                    direction_changed,
                    *filter_buffer,
                )
            )
        last = time.monotonic()

        # Small delay to keep things responsive but give time for interrupt processing.
        time.sleep(0)

        # if keys.events.get_into(keys_event):
        #     # print(keys_event)
        #     if keys_event.key_number == 1:
        #         noise += 0.5
        #     elif keys_event.key_number == 2:
        #         noise -= 0.5
        #     print("noise", noise)

        userinput.update()


except KeyboardInterrupt:
    print("exit..")
finally:
    if hasattr(board, "DISPLAY"):
        board.DISPLAY.auto_refresh = True
        board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL
