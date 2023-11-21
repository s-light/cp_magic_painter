# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

import time

from micropython import const

from configdict import extend_deep

from filter.median import MedianFilter
from filter.acceleration_direction import AccelerationDirection
from filter.acceleration_antigravity import AccelerationAntigravity

import adafruit_lis3dh

UNKNOWN = 0
REST = 10
REST_HORIZONTAL = 11
REST_VERTICAL = 12
TILTING_LEFT = 21
TILTING_RIGHT = 22
TAB_X = 31
TAB_Y = 32

gesture = {
    UNKNOWN: "UNKNOWN",
    REST: "REST",
    REST_HORIZONTAL: "REST_HORIZONTAL",
    REST_VERTICAL: "REST_VERTICAL",
    TILTING_LEFT: "TILTING_LEFT",
    TILTING_RIGHT: "TILTING_RIGHT",
    TAB_X: "TAB_X",
    TAB_Y: "TAB_y",
}


class GestureDetector(object):
    """
    GestureDetector.

    tries to detect some basic gestures and report them as events.

    planed gestures:
    - shake (with turning-point & duration)
    - horizontal rest
    - tilting from rest to left / right (around Y)
    - tap (x z)

    currently we have a basic rest detection and
    simple gravity correction.

    for the events to work its critical to start in a rest position and also end in rest.

    """

    config_defaults = {
        "gesture": {
            "filter_size": 4,
            "noise": 1.2,
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

        self.direction_x = AccelerationDirection(
            noise=self.noise,
            buffer_size=self.filter_size,
            callback_direction_changed=self.callback_gesture,
        )
        self.direction_y = AccelerationDirection(
            noise=self.noise,
            buffer_size=self.filter_size,
            callback_direction_changed=self.callback_gesture,
        )
        self.direction_z = AccelerationDirection(
            noise=self.noise,
            buffer_size=self.filter_size,
            callback_direction_changed=self.callback_gesture,
        )

        self.antigravity = AccelerationAntigravity()
        self.base = (0, 0, 0)

        self.current = UNKNOWN

        self.plot_data = False
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
        x = accel_x / adafruit_lis3dh.STANDARD_GRAVITY
        y = accel_y / adafruit_lis3dh.STANDARD_GRAVITY
        z = accel_z / adafruit_lis3dh.STANDARD_GRAVITY

        self.input_corrected = self.antigravity.update((x, y, z))

        # self.direction_x.update(x)
        # self.direction_y.update(y)
        # self.direction_z.update(z)
        # self.direction_x.update(self.input_corrected[0])
        # self.direction_y.update(self.input_corrected[1])
        # self.direction_z.update(self.input_corrected[2])

        if self.antigravity.rest_active:
            gesture_new = REST
            if z < -8:
                # holding stick *horizontal*
                gesture_new = REST_HORIZONTAL
        else:
            gesture_new = UNKNOWN

        if self.current != gesture_new:
            self.current = gesture_new
            print("new gesture:", gesture.get(self.current))
            # gesture changed..
            # event!

        if self.plot_data:
            print(
                self.filter_print_template.format(
                    time.monotonic() - self.plot_start,
                    (time.monotonic() - self.update_last_timestamp) * 1000,
                ),
                # self.direction_x.format_current_value(), # 5 values
                # self.direction_y.format_current_value(), # 5 values
                # self.direction_z.format_current_value(), # 5 values
                self.antigravity.format_current_value(),  # 12 values
            )
        self.update_last_timestamp = time.monotonic()
