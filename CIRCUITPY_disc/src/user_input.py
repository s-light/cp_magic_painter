# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

import time

import board

import touchio
import keypad
from adafruit_debouncer import Debouncer

import neopixel

import busio

import helper

from configdict import extend_deep
from gesture_detector import GestureDetector, gestures
from gesture_detector import UNKNOWN, REST, REST_HORIZONTAL


class TouchEvent(object):
    def __init__(self, *, touch_id, touch):
        self.touch_id = touch_id
        self.touch = touch

    def __str__(self):
        return "TouchEvent: id:{} touch:{}".format(self.touch_id, self.touch)


class UserInput(object):
    """UserInput."""

    config_defaults = {
        "hw": {
            "touch": {
                "pins": [
                    # board.D5,
                    # board.D6,
                    # board.D7,
                ],
                "threshold": 4000,
                "auto_calibration_delay": 30,
            },
            "accel_i2c_pins": {
                "clock": "SCL1",
                "data": "SDA1",
            },
        },
    }

    def __init__(self, *, config, callback_button, callback_touch, callback_gesture):
        super(UserInput, self).__init__()

        print("init UserInput..")

        self.config = config
        extend_deep(self.config, self.config_defaults.copy())

        # status led
        self.status_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.status_pixel.fill((0, 0, 0))

        self.callback_button = callback_button
        self.callback_touch_main = callback_touch
        self.callback_gesture_main = callback_gesture

        self.init_userInput()
        self.touch_reset_threshold()

        self.accel_sensor_init()
        self.gesture = GestureDetector(
            accel_sensor=self.accel_sensor,
            callback_gesture=self.callback_gesture,
        )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # sub init
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def init_userInput(self):
        # self.button_io = digitalio.DigitalInOut(board.BUTTON)
        # self.button_io.switch_to_input(pull=digitalio.Pull.UP)
        # self.button = Button(self.button_io)

        self.button_init()

        self.touch_init()

    def button_init(self):
        # https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython/advanced-features#avoiding-storage-allocation-3099287
        self.button = keypad.Keys(
            (board.BUTTON,),
            value_when_pressed=False,
            pull=True,
        )
        self.button_event = keypad.Event()

    def touch_init(self):
        print("touch init..")
        self.touch_active = True
        self.touch_last_action = time.monotonic()
        self.touch_auto_calibration_delay = self.config["hw"]["touch"][
            "auto_calibration_delay"
        ]

        self.touch_pins = []
        self.touch_pins_debounced = []
        for touch_id, touch_pin in enumerate(self.config["hw"]["touch"]["pins"]):
            touch = touchio.TouchIn(touch_pin)
            # initialise threshold to maximum value.
            # we later fix this..
            # we need some time passed to be able to get correct readings.
            touch.threshold = 65535
            self.touch_pins.append(touch)
            self.touch_pins_debounced.append(Debouncer(touch))
            print(
                "{:>2} {:<9}: "
                "touch.raw_value {:>5}"
                "".format(
                    touch_id,
                    str(touch_pin),
                    touch.raw_value,
                )
            )

    def accel_sensor_init(self):
        """Init the acceleration sensor."""
        self.i2c = busio.I2C(
            scl=helper.get_pin(
                config=self.config, bus_name="accel_i2c_pins", pin_name="clock"
            ),
            sda=helper.get_pin(
                config=self.config, bus_name="accel_i2c_pins", pin_name="data"
            ),
            frequency=400000,
        )
        print("i2c scan:")
        print("lock:", self.i2c.try_lock())
        i2c_address_list_hex = ["0x{:x}".format(adr) for adr in self.i2c.scan()]
        print("i2c devices:", i2c_address_list_hex)
        print("unlock:", self.i2c.unlock())
        # self.accel_sensor = slight_lsm303d_accel.LSM303D_Accel(self.i2c)

        if "0x18" in i2c_address_list_hex:
            import adafruit_lis3dh

            self.accel_sensor = adafruit_lis3dh.LIS3DH_I2C(self.i2c)
            self.accel_sensor.range = adafruit_lis3dh.RANGE_16_G
            self.accel_sensor.data_rate = (
                adafruit_lis3dh.DATARATE_LOWPOWER_5KHZ
            )  # → 0,2ms
        elif "0x62" in i2c_address_list_hex:
            from adafruit_msa3xx import MSA311

            self.accel_sensor = MSA311(self.i2c)
        elif "0x62" in i2c_address_list_hex:
            from adafruit_bno08x import (
                BNO_REPORT_ACCELEROMETER,
                BNO_REPORT_LINEAR_ACCELERATION,
                BNO_REPORT_STABILITY_CLASSIFIER,
            )
            from adafruit_bno08x.i2c import BNO08X_I2C

            self.bno = BNO08X_I2C(self.i2c)
            self.bno.enable_feature(BNO_REPORT_ACCELEROMETER)
            self.bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)
            self.bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)

            self.accel_sensor = self.bno
        else:
            raise "No Acceleration sensor found! please check your connections."

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # internal
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # touch
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def touch_reset_threshold(self):
        print("touch reset threshold")
        threshold = self.config["hw"]["touch"]["threshold"]
        for touch_id, touch in enumerate(self.touch_pins):
            print(
                "{:>2} {:<9}: "
                # "{:>5} + {:>5} = {:>5}"
                "touch.raw_value {:>5} + threshold {:>5} = {:>5}"
                "".format(
                    touch_id,
                    str(self.config["hw"]["touch"]["pins"][touch_id]),
                    touch.raw_value,
                    threshold,
                    touch.raw_value + threshold,
                )
            )
            try:
                touch.threshold = touch.raw_value + threshold
            except ValueError as e:
                print(e, "set to 65535")
                touch.threshold = 65535

    def touch_check_autocalibration(self):
        duration = time.monotonic() - self.touch_last_action
        if duration > self.touch_auto_calibration_delay:
            self.touch_reset_threshold()
            self.touch_last_action = time.monotonic()
        # TODO: implement reset on stuck touches..

    def touch_print_status(self):
        for touch_id, touch in enumerate(self.touch_pins):
            print(
                "{:>2}"
                # " {:<9}"
                ": "
                "{:>1} - {:>5}"
                "    "
                "".format(
                    touch_id,
                    # str(self.config["hw"]["touch"]["pins"][touch_id]),
                    touch.value,
                    touch.raw_value,
                ),
                end="",
            )
        print()

    def touch_update(self):
        for touch_id, touch_debounced in enumerate(self.touch_pins_debounced):
            touch_debounced.update()
            if touch_debounced.fell or touch_debounced.rose or touch_debounced.value:
                event = TouchEvent(touch_id=touch_id, touch=touch_debounced)
                self.callback_touch(event)
                self.touch_last_action = time.monotonic()
        self.touch_check_autocalibration()

    def callback_touch(self, event):
        print("callback_touch", event)
        self.status_pixel.fill((0, 100, 0))
        self.callback_touch_main(event)
        self.status_pixel.fill((0, 0, 0))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # gesture
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def callback_gesture(self, event):
        print("handle_gesture", event)
        self.callback_gesture_main(event)
        if event.gesture == UNKNOWN:
            self.status_pixel.fill((0, 0, 0))
        elif event.gesture == REST_HORIZONTAL:
            self.status_pixel.fill((0, 0, 100))
            self.touch_reset_threshold()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # main api
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self):
        # button input
        if self.button.events.get_into(self.button_event):
            if self.button_event.pressed:
                if self.button_event.key_number == 0:
                    self.callback_button()
        self.touch_update()
        # debug output
        # self.touch_print_status()
        self.gesture.update()

    def run_test(self):
        print(42 * "*")
        print("test...")
        running = True
        while running:
            try:
                self.update()
                self.touch_print_status()
                time.sleep(0.2)
            except KeyboardInterrupt as e:
                print("KeyboardInterrupt - Stop Program.", e)
                running = False


def dev_test():
    import sys

    sys.path.append("/src")
    # import user_input

    def cb_button():
        print("button pressed!")

    def cb_touch(touch_debounced):
        print("touch_debounced activated!")

    ui = UserInput(
        config={},
        callback_button=cb_button,
        callback_touch=cb_touch,
    )
    ui.run_test()


if __name__ == "__main__":
    dev_test()
