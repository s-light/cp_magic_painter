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

from rainbowio import colorwheel
import adafruit_dotstar


button_io = digitalio.DigitalInOut(board.BUTTON)
button_io.switch_to_input(pull=digitalio.Pull.UP)
button = Button(button_io)

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

board.DISPLAY.brightness = 0.01
print("deactivate display..")
board.DISPLAY.auto_refresh = False
board.DISPLAY.root_group = displayio.Group()

# time, y, delta, direction
out_template = "{:10.3f}; {:10.3f}; {:10.3f}; {:1d}"

y_last = 0
y_average = 0
noise = 0.2 
direction = 0

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
        y_average += y
        y_average /= 2

        # detect direction

        # if y_last < y:
        #     direction = +1
        #     y_last = y
        # elif y_last > y:
        #     direction = -1
        #     y_last = y
        # else:
        #     direction = 0

        if (y_last + noise) < y:
            direction = +1
            y_last = y
        elif (y_last - noise) > y:
            direction = -1
            y_last = y
        else:
            direction = 0

        # if (y_last + noise) < y_average:
        #     direction = +1
        #     y_last = y_average
        # elif (y_last - noise) > y_average:
        #     direction = -1
        # else:
        #     direction = 0

        # led test output
        if direction is 1:
            pixels[pixel_count - 1] = (0, 0, 1)
            pixels[pixel_count - 3] = (0, 0, 0)
            pixels.show()
        elif direction is -1:
            pixels[pixel_count - 1] = (0, 0, 0)
            pixels[pixel_count - 3] = (0, 1, 0)
            pixels.show()
        else:
            pixels[pixel_count - 1] = (0, 0, 0)
            pixels[pixel_count - 3] = (0, 0, 0)
            pixels.show()

        print(
            out_template.format(
                time.monotonic() - start,
                y,
                (time.monotonic() - last) * 1000,
                direction,
            )
        )
        last = time.monotonic()

        # Small delay to keep things responsive but give time for interrupt processing.
        time.sleep(0)

        button.update()
        if button.pressed:
            # reset
            pixels[pixel_count - 1] = (1, 0, 0)
            pixels[pixel_count // 2] = (1, 1, 0)
            pixels.show()
            for x in range(1000):
                print(out_template.format(0, 0, 0, 0))
            y_last = 0
            y_average = 0
            direction = 0
            pixels.fill((0, 0, 0))
            pixels.show()
            last = time.monotonic()
            start = time.monotonic()


except KeyboardInterrupt:
    print("exit..")
finally:
    board.DISPLAY.auto_refresh = True
    board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL
