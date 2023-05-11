# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_lis3dh

# uses board.SCL and board.SDA
i2c = board.I2C()
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# RANGE_2_G
# RANGE_4_G
# RANGE_8_G
# RANGE_16_G
lis3dh.range = adafruit_lis3dh.RANGE_16_G

# lis3dh.data_rate = adafruit_lis3dh.DATARATE_400_HZ # default → 2,5ms
lis3dh.data_rate = adafruit_lis3dh.DATARATE_LOWPOWER_5KHZ  # → 0,2ms

while True:
    # Read accelerometer values (in m / s ^ 2).
    # print("{:10.3f} {:10.3f} {:10.3f}".format(*lis3dh.acceleration))
    print(lis3dh.acceleration[1])

    # Small delay to keep things responsive but give time for interrupt processing.
    # 1ms = 0.0001s
    # 1us = 0.00001s
    # time.sleep(0.00001)
    time.sleep(0)
