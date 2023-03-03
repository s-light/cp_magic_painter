# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display accelerometer data once per second """

import time
import board
import slight_lsm303d_accel

import neopixel_write
import digitalio
pixel_pin = digitalio.DigitalInOut(board.NEOPIXEL)
pixel_pin.direction = digitalio.Direction.OUTPUT
neopixel_write.neopixel_write(pixel_pin, bytearray([1, 1, 1]))



import busio
i2c = busio.I2C(board.IO9, board.IO8)
sensor = slight_lsm303d_accel.LSM303D_Accel(i2c)

while True:
    # acc_x, acc_y, acc_z = sensor.acceleration

    # print(
    #     "Acceleration (m/s^2): ({0:10.3f}, {1:10.3f}, {2:10.3f})".format(
    #         acc_x, acc_y, acc_z
    #     )
    # )
    # print("")
    # time.sleep(1.0)
    acc_x, acc_y, acc_z = sensor._raw_acceleration

    # print(
    #     "{0:10d}, {1:10d}, {2:10d}".format(
    #         acc_x, acc_y, acc_z
    #     )
    # )
    # print("")

    if(acc_y > 17000):
        neopixel_write.neopixel_write(pixel_pin, bytearray([255, 0, 0]))
    elif(acc_y < -17000):
        neopixel_write.neopixel_write(pixel_pin, bytearray([0, 0, 255]))
    else:
        neopixel_write.neopixel_write(pixel_pin, bytearray([0, 1, 0]))
    # time.sleep(0.001)
