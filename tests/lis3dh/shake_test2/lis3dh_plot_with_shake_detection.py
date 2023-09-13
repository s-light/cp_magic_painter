# SPDX-FileCopyrightText: 2023 s-light.eu Stefan Krüger
# SPDX-License-Identifier: MIT

import time
import usb_cdc
import board
import busio
import digitalio
import displayio

import adafruit_lis3dh
from adafruit_debouncer import Button
import keypad

from rainbowio import colorwheel
import adafruit_dotstar

from filter import MedianFilter

button_io = digitalio.DigitalInOut(board.BUTTON)
button_io.switch_to_input(pull=digitalio.Pull.UP)
button = Button(button_io)

plot_data = True

# https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython/advanced-features#avoiding-storage-allocation-3099287
keys = keypad.Keys(
    (board.D1, board.D2),
    value_when_pressed=True,
    pull=False,
)
keys_event = keypad.Event()

pixel_count = 36
pixels = adafruit_dotstar.DotStar(
    board.D11,
    board.D10,
    pixel_count,
    brightness=1,
    auto_write=False,
)


i2c = board.I2C()
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# RANGE_2_G
# RANGE_4_G
# RANGE_8_G
# RANGE_16_G
lis3dh.range = adafruit_lis3dh.RANGE_16_G

# default → 2,5ms update rate
lis3dh.data_rate = adafruit_lis3dh.DATARATE_400_HZ


# time; delta; direction_raw; y; y_filtered
out_template = "{:10.3f}; {:10.3f}; {:1d}; {:10.3f}; {:10.3f}"

y_last = 0
y_filtered = 0
noise = 2.1
direction_raw = 0
direction_raw_last = 0
# direction_filtered = 0
# direction_filtered_last = 0

MedianFilter

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# prepare

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

        # build running average
        
        y_filtered += y
        y_filtered /= 2

        # detect direction_raw

        # if y_last < y:
        #     direction_raw = +1
        #     y_last = y
        # elif y_last > y:
        #     direction_raw = -1
        #     y_last = y
        # else:
        #     direction_raw = 0

        if (y_last + noise) < y:
            direction_raw = +1
            y_last = y
        elif (y_last - noise) > y:
            direction_raw = -1
            y_last = y
        else:
            direction_raw = 0

        # if direction_filtered_last is not direction_raw
        # if direction_raw_last is not direction_raw :
        #     direction_raw_last = direction_raw
        #     # event! we change

        # if (y_last + noise) < y_filtered:
        #     direction_raw = +1
        #     y_last = y_filtered
        # elif (y_last - noise) > y_filtered:
        #     direction_raw = -1
        # else:
        #     direction_raw = 0

        # led test output
        if direction_raw is 1:
            pixels[pixel_count - 1] = (0, 0, 10)
            pixels[pixel_count - 3] = (0, 0, 0)
            pixels.show()
        elif direction_raw is -1:
            pixels[pixel_count - 1] = (0, 0, 0)
            pixels[pixel_count - 3] = (0, 10, 0)
            pixels.show()
        else:
            pixels[pixel_count - 1] = (0, 0, 0)
            pixels[pixel_count - 3] = (0, 0, 0)
            pixels.show()

        if plot_data:
            print(
                out_template.format(
                    time.monotonic() - start,
                    (time.monotonic() - last) * 1000,
                    direction_raw,
                    y,
                    y_filtered,
                )
            )
        last = time.monotonic()

        # Small delay to keep things responsive but give time for interrupt processing.
        time.sleep(0)

        if keys.events.get_into(keys_event):
            # print(keys_event)
            if keys_event.key_number == 1:
                noise += 0.5
            elif keys_event.key_number == 2:
                noise -= 0.5
            print("noise", noise)

        button.update()
        if button.short_count == 1:
            plot_data = not plot_data
            print("\n"*10)
            print("toggle plot_data", plot_data)
            print("\n"*10)
        elif button.short_count == 2:
            # reset
            pixels[pixel_count - 1] = (1, 0, 0)
            pixels[pixel_count // 2] = (1, 1, 0)
            pixels.show()
            for x in range(1000):
                print(out_template.format(0, 0, 0, 0, 0))
            y_last = 0
            y_filtered = 0
            direction_raw = 0
            pixels.fill((0, 0, 0))
            pixels.show()
            last = time.monotonic()
            start = time.monotonic()


except KeyboardInterrupt:
    print("exit..")
finally:
    board.DISPLAY.auto_refresh = True
    board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL
