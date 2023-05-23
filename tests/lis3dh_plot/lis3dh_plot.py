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

button_io = digitalio.DigitalInOut(board.BUTTON)
button_io.switch_to_input(pull=digitalio.Pull.UP)
button = Button(button_io)

i2c = board.I2C()
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# RANGE_2_G
# RANGE_4_G
# RANGE_8_G
# RANGE_16_G
lis3dh.range = adafruit_lis3dh.RANGE_16_G

# default → 2,5ms update rate
lis3dh.data_rate = adafruit_lis3dh.DATARATE_400_HZ


print("deactivate display..")
board.DISPLAY.auto_refresh = False
board.DISPLAY.root_group = displayio.Group()

out_template = "{:10.3f}; {:10.3f}; {:10.3f}; {:10.3f}"

# start = time.monotonic()
last = time.monotonic()
try:
    while True:
        # print single accelerometer value (in m / s ^ 2).
        # print("{:10.3f}".format(lis3dh.acceleration[1])),
        # print(lis3dh.acceleration[1])
        # usb_cdc.console.write(bytes(int(lis3dh.acceleration[1]*10)))

        # Divide them by 9.806 to convert to Gs.
        x, y, z = [
            value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
        ]
        print(out_template.format(x, y, z, (time.monotonic() - last) * 1000))
        last = time.monotonic()

        # Small delay to keep things responsive but give time for interrupt processing.
        time.sleep(0)

        button.update()
        if button.pressed:
            # reset
            for x in range(1000):
                print(out_template.format(0, 0, 0, 0))
            last = time.monotonic()
            # time.sleep(1)

except KeyboardInterrupt:
    print("exit..")
finally:
    board.DISPLAY.auto_refresh = True
    board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL
