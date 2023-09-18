# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_lis3dh

# uses board.SCL and board.SDA
i2c = board.I2C()
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_16_G

# setup reading speed
# https://docs.circuitpython.org/projects/lis3dh/en/latest/api.html#adafruit_lis3dh.LIS3DH.data_rate
# DATARATE_400_HZ → 2.5ms interval → DEFAULT
# DATARATE_200_HZ → 5ms interval
# DATARATE_100_HZ → 10ms interval
# DATARATE_50_HZ
# DATARATE_25_HZ
# DATARATE_10_HZ
# DATARATE_1_HZ
# DATARATE_POWERDOWN
# DATARATE_LOWPOWER_1K6HZ
# DATARATE_LOWPOWER_5KHZ
# lis3dh.data_rate = DATARATE_400_HZ
print("lis3dh.data_rate", lis3dh.data_rate)

# Loop forever printing accelerometer values
while True:
    # Read accelerometer values (in m / s ^ 2).
    # Returns a 3-tuple of x, y, z axis values.

    # print("x = %0.3f m/s^2, y = %0.3f m/s^2, z = %0.3f m/s^2" % (*lis3dh.acceleration))
    # print("%0.3f, %0.3f, %0.3f" % (*lis3dh.acceleration))

    # Divide them by 9.806 to convert to Gs.
    # x, y, z = [
    #     value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
    # ]
    # print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))

    # print(
    #     "X: {: > 10.6f}  Y: {: > 10.6f} Z: {: > 10.6f}  m/s^2".format(
    #  *lis3dh.acceleration
    #     )
    # )
    print("{:10.3f} {:10.3f} {:10.3f}".format(*lis3dh.acceleration))

    # Small delay to keep things responsive but give time for interrupt processing.
    time.sleep(0.001)
