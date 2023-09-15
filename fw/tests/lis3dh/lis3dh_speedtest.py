# based on example
# https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH/blob/main/examples/lis3dh_simpletest.py
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import displayio
import busio
import adafruit_lis3dh

# uses board.SCL and board.SDA
if hasattr(board, "STEMMA_I2C"):
    i2c = board.STEMMA_I2C()
elif hasattr(board, "I2C"):
    i2c = board.I2C()
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# RANGE_2_G
# RANGE_4_G
# RANGE_8_G
# RANGE_16_G
lis3dh.range = adafruit_lis3dh.RANGE_16_G


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
            "'{:<" + "{}".format(msg_max_length + 5) + "}'  needs {:10.3f}ms/call"
        )
        print(
            msg_template.format(
                test["msg"],
                test["duration_ms"],
            )
        )


print("\n" * 20)
speed_tests = []


# lis3dh.data_rate = adafruit_lis3dh.DATARATE_1_HZ  # default → 1000ms
# speed_tests.append(
#     speed_test(
#         lambda: lis3dh.acceleration[1],
#         msg="lis3dh.acceleration[1] → 1Hz (1000ms)",
#     )
# )

lis3dh.data_rate = adafruit_lis3dh.DATARATE_400_HZ  # default → 2,5ms
speed_tests.append(
    speed_test(
        lambda: lis3dh.acceleration[1],
        msg="lis3dh.acceleration[1] → 400Hz (2.5ms)",
    )
)


# lis3dh.data_rate = adafruit_lis3dh.DATARATE_LOWPOWER_5KHZ  # → 0,2ms
# speed_tests.append(
#     speed_test(
#         lambda: lis3dh.acceleration[1],
#         msg="lis3dh.acceleration[1] → 5kHz (0,2ms)",
#     )
# )


speed_tests.append(
    speed_test(
        lambda: print(3.14159),
        msg="print(i * 3.14159)",
    )
)

lis3dh.data_rate = adafruit_lis3dh.DATARATE_400_HZ  # default → 2,5ms

speed_tests.append(
    speed_test(
        lambda: print(lis3dh.acceleration[1]),
        msg="print(lis3dh.acceleration[1]) 400Hz",
        count=50,
    )
)




# ++++++++++++++++++++++++++++++++++++++++++
#  now with High Speed / without Display
# ++++++++++++++++++++++++++++++++++++++++++


msg=" fastI2C"
if hasattr(board, "DISPLAY"):
    print("deactivate display..")
    board.DISPLAY.auto_refresh = False
    board.DISPLAY.root_group = displayio.Group()
    msg=" no display"

i2c.deinit()
if hasattr(board, "STEMMA_I2C"):
    i2c = busio.I2C(scl=board.SCL1, sda=board.SDA1, frequency=400000)
elif hasattr(board, "I2C"):
    i2c = busio.I2C(scl=board.SCL, sda=board.SDA, frequency=400000)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)


speed_tests.append(
    speed_test(
        lambda: print(lis3dh.acceleration[1]),
        msg="print(lis3dh.acceleration[1]) 400Hz" + msg,
    )
)

speed_tests.append(
    speed_test(
        lambda: print(lis3dh.read_adc_raw(1)),
        msg="print(lis3dh.read_adc_raw(1)) 400Hz" + msg,
    )
)

speed_tests.append(
    speed_test(
        lambda: print(3.14159),
        msg="print(i * 3.14159)" + msg,
    )
)

speed_tests.append(
    speed_test(
        lambda: print("{:10.3f}".format(lis3dh.acceleration[1])),
        msg='print("{:10.3f}".format(lis3dh.acceleration[1])) 400Hz' + msg,
    )
)

speed_tests.append(
    speed_test(
        lambda: print("{:10.3f} {:10.3f} {:10.3f}".format(*lis3dh.acceleration)),
        msg='print("{:10.3f} {:10.3f} {:10.3f}".format(*lis3dh.acceleration)) 400Hz' + msg,
    )
)



lis3dh.data_rate = adafruit_lis3dh.DATARATE_LOWPOWER_5KHZ  # → 0,2ms
speed_tests.append(
    speed_test(
        lambda: print(lis3dh.read_adc_raw(1)),
        msg="print(lis3dh.read_adc_raw(1)) 5kHz" + msg,
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
