# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

import time

from configdict import extend_deep

from filter.median import MedianFilter
from filter.acceleration_direction import AccelerationDirection

import adafruit_lis3dh


class GestureDetector(object):
    """GestureDetector."""

    config_defaults = {
        "gesture": {
            "filter_size": 4,
            "noise": 1.0,
        },
    }
    filter_print_template = "{:7.3f}; " "{:7.3f}; "  # plot_runtim  # update duration

    def __init__(self, *, config={}, callback_gesture, accel_sensor):
        super(GestureDetector, self).__init__()

        print("init GestureDetector..")

        self.config = config
        extend_deep(self.config, self.config_defaults.copy())

        self.accel_sensor = accel_sensor
        self.callback_gesture = callback_gesture

        self.noise = self.config["gesture"]["noise"]
        self.filter_size = self.config["gesture"]["filter_size"]

        self.direction_y = AccelerationDirection(
            noise=self.noise,
            buffer_size=self.filter_size,
            callback_direction_changed=self.callback_gesture,
        )

        self.plot_data = True
        self.plot_start = 0
        self.update_last_timestamp = 0

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # sub init
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # internal helper
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # gesture
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def print_values(self):
        accel_x, accel_y, accel_z = self.accel_sensor.acceleration
        print(
            # "{:7.3f};    "
            "{:7.3f}; {:7.3f}; {:7.3f};    "
            "".format(
                # time.monotonic(),
                accel_x,
                accel_y,
                accel_z,
            )
        )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # main api
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self):
        accel_x, accel_y, accel_z = self.accel_sensor.acceleration

        # Divide them by 9.806 to convert to Gs.
        y = accel_y / adafruit_lis3dh.STANDARD_GRAVITY

        # self.callback_gesture
        self.direction_y.update(y)

        if self.plot_data:
            print(
                self.filter_print_template.format(
                    time.monotonic() - self.plot_start,
                    (time.monotonic() - self.update_last_timestamp) * 1000,
                ),
                self.direction_y.format_current_value(),
            )
        self.update_last_timestamp = time.monotonic()


def median_average(input_list, window_size=0.5):
    sorted_list = input_list.sort()
    window_size_el_count = len(sorted_list) * window_size
    window_start = window_size_el_count
    window_end = len(sorted_list) - window_size_el_count
    return average(sorted_list[window_start:window_end])
