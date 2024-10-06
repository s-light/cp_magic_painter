# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

import time
import board
import busio
import displayio
import adafruit_lis3dh

i2c = board.STEMMA_I2C()
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_16_G

# setup reading speed
# https://docs.circuitpython.org/projects/lis3dh/en/latest/api.html#adafruit_lis3dh.LIS3DH.data_rate
# 2.5ms interval → DEFAULT
# lis3dh.data_rate = DATARATE_400_HZ
# 0.02ms interval
# lis3dh.data_rate = DATARATE_LOWPOWER_5KHZ
print("lis3dh.data_rate", lis3dh.data_rate)

direction_old = 0
start_time = 0
duration = 0

if hasattr(board, "DISPLAY"):
    print("deactivate display..")
    board.DISPLAY.auto_refresh = False
    board.DISPLAY.root_group = displayio.Group()

average_forth_sum = 1
average_forth_count = 1
average_back_sum = 1
average_back_count = 1

debug_out_timestamp = 0
debug_out_interval = 2

def average_reset():
    global average_forth_sum
    global average_forth_count
    global average_back_sum
    global average_back_count
    average_forth_sum = 1
    average_forth_count = 1
    average_back_sum = 1
    average_back_count = 1


def main_loop():
    global direction_old
    global start_time
    global duration
    global debug_out_timestamp
    global debug_out_interval
    global average_forth_sum
    global average_forth_count
    global average_back_sum
    global average_back_count
    while True:
        # Read accelerometer values (in m / s ^ 2).
        # Returns a 3-tuple of x, y, z axis values.
        y = lis3dh.acceleration[1]
        if y > 5 and direction_old is not 1:
            direction_old = 1
            duration = (time.monotonic() - start_time) * 1000
            start_time = time.monotonic()
            # print('→ {:7.3f}'.format(duration))
            average_forth_sum += duration
            average_forth_count += 1
        if y < -5 and direction_old is not 0:
            direction_old = 0
            duration = (time.monotonic() - start_time) * 1000
            start_time = time.monotonic()
            # print('← {:7.3f}'.format(duration))
            average_back_sum += duration
            average_back_count += 1

        time.sleep(0.0001)

        current_duration = time.monotonic() - debug_out_timestamp
        if current_duration > debug_out_interval:
            print('→ {:7.3f} ({})'.format(average_forth_sum/average_forth_count, average_forth_count))
            print('← {:7.3f} ({})'.format(average_back_sum/average_back_count, average_back_count))
            debug_out_timestamp = time.monotonic()
            average_reset()


try:
    print("enter main_loop...")
    main_loop()
except KeyboardInterrupt:
    print("exit..")
finally:
    if hasattr(board, "DISPLAY"):
        board.DISPLAY.auto_refresh = True
        board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL
