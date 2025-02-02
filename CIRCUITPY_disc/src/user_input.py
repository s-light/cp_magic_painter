# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

import time

import board

import digitalio
import touchio
import keypad
from adafruit_debouncer import Debouncer

import neopixel

import busio

import ansi_escape_code as terminal
import nonblocking_serialinput as nb_serial

import helper

from configdict import extend_deep
from gesture_detector import GestureDetector, gestures
from gesture_detector import (
    UNKNOWN,
    REST,
    REST_HORIZONTAL,
    REST_VERTICAL,
    TILT_LEFT,
    TILT_RIGHT,
    TAB_X,
    TAB_Y,
    TAB_Z,
    DIRECTION_CHANGED,
    SHAKE_X,
    SHAKE_Y,
    SHAKE_Z,
)


class AccelerationSensorNotFound(TypeError):
    pass


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
            "button": {
                "pins": [
                    # board.A0,
                    # board.A1,
                    # board.A2,
                    # board.D5,
                    # board.D6,
                    # board.D7,
                    # board.D8,
                    # board.D9,
                    # board.D17,
                    # board.D18,
                ],
                "pin_gnd": board.D8,
            },
            "accel_i2c_pins": {
                "clock": "SCL1",
                "data": "SDA1",
            },
        },
    }

    def __init__(
        self, *, config, magicpainter, callback_button, callback_touch, callback_gesture
    ):
        super(UserInput, self).__init__()
        self.print = print
        self.print("init UserInput..")

        self.config = config
        ##########################################
        # handle board specific i2c pin usage

        if not self.config.get("hw"):
            self.config["hw"] = {
                "accel_i2c_pins": {
                    "clock": "SCL",
                    "data": "SDA",
                }
            }

            if "qtpy_esp32s3" in board.board_id:
                self.config["hw"]["accel_i2c_pins"] = {
                    "clock": "SCL1",
                    "data": "SDA1",
                }
        extend_deep(self.config, self.config_defaults.copy())

        self.magicpainter = magicpainter

        # this also sets self.print
        self.setup_serial()

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
            print_fn=self.print,
        )
        # self.gesture.plot_data = True

        self.touch_active = False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # sub init
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def init_userInput(self):
        self.button_init()

        self.touch_init()

    def button_init(self):
        print("button_init..")
        # https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython/advanced-features#avoiding-storage-allocation-3099287
        button_list = [board.BUTTON]
        button_list.extend(self.config["hw"]["button"]["pins"])
        print("  button_list", button_list)

        self.button_GND = digitalio.DigitalInOut(self.config["hw"]["button"]["pin_gnd"])
        self.button_GND.switch_to_output()
        self.button_GND.value = 0

        self.button = keypad.Keys(
            button_list,
            value_when_pressed=False,
            pull=True,
        )
        self.button_event = keypad.Event()

    def touch_init(self):
        print("touch_init..")
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
        print(f"setup {len(self.touch_pins)} touch inputs.")

    def accel_sensor_init(self):
        """Init the acceleration sensor."""
        print("accel_sensor_init..")
        self.i2c = busio.I2C(
            scl=helper.get_pin(
                config=self.config, bus_name="accel_i2c_pins", pin_name="clock"
            ),
            sda=helper.get_pin(
                config=self.config, bus_name="accel_i2c_pins", pin_name="data"
            ),
            frequency=400000,
        )
        print("  i2c scan:")
        print("  lock:", self.i2c.try_lock())
        i2c_address_list_hex = ["0x{:x}".format(adr) for adr in self.i2c.scan()]
        print("  i2c devices:", i2c_address_list_hex)
        print("  unlock:", self.i2c.unlock())
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
            raise AccelerationSensorNotFound(
                "No Acceleration sensor found! please check your connections."
            )

    def setup_serial(self):
        # make some space so that nothing is overwritten...
        print("\n" * 4)
        print("user_input setup_serial")
        self.my_input = nb_serial.NonBlockingSerialInput(
            input_handling_fn=self.userinput_event_handling,
            print_help_fn=self.userinput_print_help,
            echo=True,
            statusline=True,
            statusline_intervall=1.0,
            statusline_fn=self.statusline_fn,
        )
        self.print = self.my_input.print
        self.magicpainter.print = self.my_input.print

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # internal
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # touch
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def touch_reset_threshold(self):
        # print("touch reset threshold")
        threshold = self.config["hw"]["touch"]["threshold"]
        for touch_id, touch in enumerate(self.touch_pins):
            # print(
            #     "{:>2} {:<9}: "
            #     # "{:>5} + {:>5} = {:>5}"
            #     "touch.raw_value {:>5} + threshold {:>5} = {:>5}"
            #     "".format(
            #         touch_id,
            #         str(self.config["hw"]["touch"]["pins"][touch_id]),
            #         touch.raw_value,
            #         threshold,
            #         touch.raw_value + threshold,
            #     )
            # )
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
        if self.touch_active:
            for touch_id, touch_debounced in enumerate(self.touch_pins_debounced):
                touch_debounced.update()
                if (
                    touch_debounced.fell
                    or touch_debounced.rose
                    or touch_debounced.value
                ):
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
    # buttons
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def button_update(self):
        # button input
        if self.button.events.get_into(self.button_event):
            self.callback_button(self.button_event)
            # if self.button_event.pressed:
            # if self.button_event.key_number == 0:
            #     self.callback_button()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # gesture
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def callback_gesture(self, event):
        # self.print("handle_gesture", event)
        self.touch_active = False
        if event.gesture == REST:
            self.status_pixel.fill((0, 1, 0))
        elif event.gesture == REST_HORIZONTAL:
            self.status_pixel.fill((0, 10, 0))
            self.touch_reset_threshold()
            self.touch_active = True
        elif event.gesture == DIRECTION_CHANGED:
            # self.print(event)
            if event.orig_event.instance.axis_name == "y":
                direction = event.orig_event.direction
                if direction == +1:
                    self.status_pixel.fill((1, 0, 0))
                elif direction == -1:
                    self.status_pixel.fill((0, 0, 1))
        elif event.gesture == TILT_LEFT:
            self.status_pixel.fill((10, 10, 0))
        elif event.gesture == TILT_RIGHT:
            self.status_pixel.fill((0, 10, 10))
        # elif event.gesture  == TAB_Z:
        #     self.status_pixel.fill((0, 0, 200))
        elif event.gesture in [SHAKE_X, SHAKE_Z, TAB_X, TAB_Y, TAB_Z]:
            self.print(event)
        # elif event.gesture == UNKNOWN:
        #     print(event)
        else:
            self.status_pixel.fill((0, 0, 0))

        self.callback_gesture_main(event)

    ##########################################
    # menu

    def userinput_print_help(self):
        """Print Help."""
        self.print(
            "you can set some options:\n"
            "- 'mode': toggle system mode [rgblamp | povpainter] ({mode})\n"
            "- 'plot': toggle data plot ({plot})\n"
            # "- 'xy':  ({heater_target: > 7.2f})\n"
            # "- 'pn' select next profil\n"
            # "{profile_list}"
            # "- 'stop'  reflow cycle\n"
            "".format(
                mode=self.magicpainter.mode.__name__, plot=self.gesture.plot_data
            ),
            # end="",
        )

    def userinput_event_handling(self, input_string):
        """Check Input."""
        if input_string.startswith("?"):
            self.print("help:\n todo!\n please look at the source code for now...")
        elif input_string.startswith("mode"):
            self.magicpainter.switch_to_next_mode()
        elif input_string.startswith("plot"):
            self.gesture.plot_data = not self.gesture.plot_data
            # if "rgb" in input_string or "pov" in input_string:
        # elif input_string.startswith("stop"):
        #     self.menu_reflowcycle_stop()

    statusline_template = (
        "{uptime: >8.2f} "
        "gesture:{gesture:>16s} "
        "{y_active_color}y: "
        "{y_dir:+} "
        "{y_stable} "
        "{y_freq:>4.2f}Hz "
        "{reset}"
        "{fg_blue}{mode: >10}{reset}: "
        "b: {fg_orange}{brightness: >4.2f}{reset} "
        # "brightness: {brightness: >4.2f} "
    )

    def statusline_fn(self):
        """
        Generate statusline.
        """
        # NO prints in this function!!
        # (leads to infinity loops..)

        # this does not work in that easy way...
        # current_color = terminal.ANSIColors.fg.lightblue
        # current_color = terminal.ANSIColors.fg.orange

        # if self.reflowcontroller.temperature_changed:
        #     # self.reflowcontroller.temperature_changed = False
        #     # print("\n" * 5 + "tch" + "\n" * 5)

        y_stable = False
        y_active_color = terminal.ANSIColors.fg.darkgrey
        if self.gesture.direction_y.shake_active:
            y_active_color = terminal.ANSIColors.fg.pink
            y_stable = self.gesture.direction_y.durations.forward_avg.stable

        # print(
        #     "brightness:",
        #     self.magicpainter.mode.brightness,
        # )
        statusline = self.statusline_template.format(
            uptime=time.monotonic(),
            # gesture
            gesture=gestures.get(self.gesture.current),
            y_active_color=y_active_color,
            y_dir=self.gesture.direction_y.direction_raw,
            y_stable=y_stable,
            y_freq=(1 / self.gesture.direction_y.durations.forward_avg.average),
            # brightness
            brightness=self.magicpainter.mode.brightness,
            # mode
            mode=self.magicpainter.mode.__name__,
            # color helper
            reset=terminal.ANSIColors.reset,
            fg_orange=terminal.ANSIColors.fg.orange,
            fg_blue=terminal.ANSIColors.fg.blue,
        )
        statusline += self.magicpainter.mode.statusline_fn()

        return statusline

    # @staticmethod
    # def input_parse_pixel_set(input_string):
    #     """parse pixel_set."""
    #     # row = 0
    #     # col = 0
    #     # value = 0
    #     # sep_pos = input_string.find(",")
    #     # sep_value = input_string.find(":")
    #     # try:
    #     #     col = int(input_string[1:sep_pos])
    #     # except ValueError as e:
    #     #     self.print("Exception parsing 'col': ", e)
    #     # try:
    #     #     row = int(input_string[sep_pos + 1 : sep_value])
    #     # except ValueError as e:
    #     #     self.print("Exception parsing 'row': ", e)
    #     # try:
    #     #     value = int(input_string[sep_value + 1 :])
    #     # except ValueError as e:
    #     #     self.print("Exception parsing 'value': ", e)
    #     # pixel_index = 0
    #     pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # main api
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self):
        self.button_update()
        self.touch_update()
        # debug output
        # self.touch_print_status()
        self.gesture.update()
        self.my_input.update()

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
