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
TILT_LEFT = 21
TILT_RIGHT = 22
TAB_X = 31
TAB_Y = 32
TAB_Z = 33
DIRECTION_CHANGED = 40
SHAKE_X = 41
SHAKE_Y = 42
SHAKE_Z = 43

gestures = {
    UNKNOWN: "UNKNOWN",
    REST: "REST",
    REST_HORIZONTAL: "REST_HORIZONTAL",
    REST_VERTICAL: "REST_VERTICAL",
    TILT_LEFT: "TILT_LEFT",
    TILT_RIGHT: "TILT_RIGHT",
    TAB_X: "TAB_X",
    TAB_Y: "TAB_Y",
    TAB_Z: "TAB_Z",
    DIRECTION_CHANGED: "DIRECTION_CHANGED",
    SHAKE_X: "SHAKE_X",
    SHAKE_Y: "SHAKE_Y",
    SHAKE_Z: "SHAKE_Z",
}


class GestureEvent(object):
    def __init__(self, *, gesture, gesture_last=None, orig_event=None):
        self.gesture = gesture
        self.gesture_last = gesture_last
        self.orig_event = orig_event

    def __str__(self):
        if self.orig_event:
            # return "gesture: {} \n orig_event: {}".format(
            return "gesture: {} orig_event: {}".format(
                gestures.get(self.gesture), self.orig_event
            )
        else:
            return gestures.get(self.gesture)


class GestureDetector(object):
    """
    GestureDetector.

    detect some basic gestures and report them as events.

    planed gestures:
    - shake (with turning-point & duration)
    - horizontal rest
    - tilting from rest to left / right (around Y)
    - tap (x z)

    currently we have a basic rest detection and
    simple gravity 'correction'.

    for the events to work its critical to start in a rest position and also end in rest.

    """

    config_defaults = {
        "gesture": {
            "filter_size": 4,
            "noise": 1.2,
        },
    }
    filter_print_template = "{:7.3f}; " "{:7.3f}; "  # plot_runtime  # update duration

    def __init__(self, *, config={}, print_fn, callback_gesture, accel_sensor):
        super(GestureDetector, self).__init__()
        self.print = print
        self.print("init GestureDetector..")

        self.config = config
        extend_deep(self.config, self.config_defaults.copy())

        self.accel_sensor = accel_sensor
        self.callback_gesture = callback_gesture

        self.noise = self.config["gesture"]["noise"]
        self.filter_size = self.config["gesture"]["filter_size"]

        self.stable_threshold = 0.10

        self.direction_x = AccelerationDirection(
            noise=self.noise,
            buffer_size=self.filter_size,
            callback_direction_changed=self.callback_direction_changed,
            axis_name="x",
            stable_threshold=self.stable_threshold,
        )
        self.direction_y = AccelerationDirection(
            noise=self.noise,
            buffer_size=self.filter_size,
            callback_direction_changed=self.callback_direction_changed,
            axis_name="y",
            stable_threshold=self.stable_threshold,
        )
        self.direction_z = AccelerationDirection(
            # noise=self.noise,
            noise=2.0,
            buffer_size=self.filter_size,
            callback_direction_changed=self.callback_direction_changed,
            axis_name="z",
            stable_threshold=self.stable_threshold,
        )

        self.antigravity = AccelerationAntigravity()
        self.base = (0, 0, 0)

        self.last = UNKNOWN
        self.current = UNKNOWN

        self.plot_data = False
        self.plot_start = 0
        self.update_last_timestamp = 0

        self.print = print_fn

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # sub init
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # internal helper
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def callback_direction_changed(self, event):
        # if event.instance.axis_name == "x":
        #     gesture_event = GestureEvent(gesture=SHAKE_X, orig_event=event)
        # elif event.instance.axis_name == "z":
        #     gesture_event = GestureEvent(gesture=SHAKE_Z, orig_event=event)
        # else:
        #     gesture_event = GestureEvent(gesture=DIRECTION_CHANGED, orig_event=event)
        gesture_event = GestureEvent(
            gesture=DIRECTION_CHANGED,
            gesture_last=self.current,
            orig_event=event,
        )
        self.callback_gesture(gesture_event)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # gesture
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def print_values(self):
        accel_x, accel_y, accel_z = self.accel_sensor.acceleration
        self.print(
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

        self.direction_x.update(x)
        self.direction_y.update(y)
        self.direction_z.update(z)
        # self.direction_x.update(self.input_corrected[0])
        # self.direction_y.update(self.input_corrected[1])
        # self.direction_z.update(self.input_corrected[2])
        x_avg = self.direction_x.avg0
        y_avg = self.direction_y.avg0
        z_avg = self.direction_z.avg0

        plot_data_single = False
        gesture_new = self.current

        if self.antigravity.rest_active:
            if (
                (-0.22 < x_avg < 0.22)
                and (-0.22 < y_avg < 0.22)
                and (-1.3 < z_avg < -0.8)
            ):
                gesture_new = REST_HORIZONTAL
            elif (
                (-0.2 < x_avg < 0.2) and (-1.3 < y_avg < -0.9) and (-0.2 < z_avg < 0.2)
            ):
                gesture_new = TILT_LEFT
            elif (-0.2 < x_avg < 0.2) and (0.9 < y_avg < 1.3) and (-0.2 < z_avg < 0.2):
                gesture_new = TILT_RIGHT
            else:
                gesture_new = REST

            # if self.current != gesture_new:
            #     plot_data_single = True
        else:
            gesture_new = UNKNOWN

        if self.current != gesture_new:
            self.last = self.current
            self.current = gesture_new
            event = GestureEvent(
                gesture=self.current,
                gesture_last=self.last,
            )
            self.callback_gesture(event)
            # plot_data_single = True

        # if self.plot_data:
        if self.plot_data or plot_data_single:
            self.print(
                self.filter_print_template.format(
                    time.monotonic() - self.plot_start,
                    (time.monotonic() - self.update_last_timestamp) * 1000,
                ),
                # self.direction_x.format_current_value(),  # 5 values
                # self.direction_y.format_current_value(),  # 5 values
                # self.direction_z.format_current_value(),  # 5 values
                # self.antigravity.format_current_value(),  # 12 values
                "{:7.3f}; {:7.3f}; {:7.3f}; ".format(x_avg, y_avg, z_avg),
            )
        self.update_last_timestamp = time.monotonic()
