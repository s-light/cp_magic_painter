# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    # BNO_REPORT_GYROSCOPE,
    # BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_LINEAR_ACCELERATION,
    # BNO_REPORT_ROTATION_VECTOR,
    # BNO_REPORT_GAME_ROTATION_VECTOR,
    # BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR,
    # BNO_REPORT_STEP_COUNTER,
    # BNO_REPORT_RAW_ACCELEROMETER,
    # BNO_REPORT_RAW_GYROSCOPE,
    # BNO_REPORT_RAW_MAGNETOMETER,
    # BNO_REPORT_SHAKE_DETECTOR,
    # BNO_REPORT_STABILITY_CLASSIFIER,
    # BNO_REPORT_ACTIVITY_CLASSIFIER,
    # BNO_REPORT_GYRO_INTEGRATED_ROTATION_VECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)

bno.enable_feature(BNO_REPORT_ACCELEROMETER)
# bno.enable_feature(BNO_REPORT_GYROSCOPE)
# bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)
# bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
# bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR)
# bno.enable_feature(BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)
# bno.enable_feature(BNO_REPORT_STEP_COUNTER)
# bno.enable_feature(BNO_REPORT_RAW_ACCELEROMETER)
# bno.enable_feature(BNO_REPORT_RAW_GYROSCOPE)
# bno.enable_feature(BNO_REPORT_RAW_MAGNETOMETER)
# bno.enable_feature(BNO_REPORT_SHAKE_DETECTOR)
# bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)
# bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)
# bno.enable_feature(BNO_REPORT_GYRO_INTEGRATED_ROTATION_VECTOR)

while True:
    time.sleep(0.1)
    # print("Acceleration:")
    # accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
    accel_x, accel_y, accel_z = bno.linear_acceleration  # pylint:disable=no-member
    print(
        "X: {: > 10.6f}  Y: {: > 10.6f} Z: {: > 10.6f}  m/s^2".format(
            accel_x, accel_y, accel_z
        )
    )
    # print("")

    # print("Gyro:")
    # gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
    # print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (gyro_x, gyro_y, gyro_z))
    # print("")

    # print("Magnetometer:")
    # mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
    # print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
    # print("")

    # print("Rotation Vector Quaternion:")
    # quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
    # print(
    #     "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real)
    # )
    # print("")
