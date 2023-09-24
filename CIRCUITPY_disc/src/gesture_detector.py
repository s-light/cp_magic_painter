# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

import time

from configdict import extend_deep

from filter.median import MedianFilter


class GestureDetector(object):
    """GestureDetector."""

    config_defaults = {
        "gesture": {},
    }

    def __init__(self, *, config={}, callback_gesture, accel_sensor):
        super(GestureDetector, self).__init__()

        print("init GestureDetector..")

        self.config = config
        extend_deep(self.config, self.config_defaults.copy())

        self.accel_sensor = accel_sensor
        self.callback_gesture = callback_gesture
        
        self.filter_init()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # sub init
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def filter_init(self):
        """Init all filters."""
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # internal
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

        self.print_values()
