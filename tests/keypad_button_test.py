# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT
# source https://github.com/s-light/cp_magic_painter/


"""
# simple keypad button test


## HW: 
- Adafruit QT Py ESP32-S3 https://www.adafruit.com/product/5426

"""

# import os
import sys


import gc
import time

import board
import busio
import digitalio

import json

from src.configdict import extend_deep

import keypad

# button = digitalio.DigitalInOut(board.BUTTON)
# button.switch_to_input(pull=digitalio.Pull.UP)

##########################################
# main class


class ButtonTest(object):
    """ButtonTest."""

    config_defaults = {
        # all sub default parts are defined in the modules themselfes..
    }
    config = {}

    def __init__(self):
        super(ButtonTest, self).__init__()
        # self.print is later replaced by the ui module.
        self.print = lambda *args: print(*args)

        self.print("ButtonTest")
        self.print("  https://github.com/s-light/cp_magic_painter")
        self.print(42 * "*")

        self.load_config()

        self.init_userInput()

    def load_config(self, filename="/config.json"):
        self.config = {}
        try:
            with open(filename, mode="r") as configfile:
                self.config = json.load(configfile)
                configfile.close()
        except OSError as e:
            # self.print(dir(e))
            # self.print(e.errno)
            if e.errno == 2:
                self.print(e)
                # self.print(e.strerror)
            else:
                raise e
        # extend with default config - thisway it is safe to use ;-)
        extend_deep(self.config, self.config_defaults.copy())

    def init_userInput(self):
        # self.button_io = digitalio.DigitalInOut(board.BUTTON)
        # self.button_io.switch_to_input(pull=digitalio.Pull.UP)
        # self.button = Button(self.button_io)

        # https://learn.adafruit.com/key-pad-matrix-scanning-in-circuitpython/advanced-features#avoiding-storage-allocation-3099287
        self.button = keypad.Keys(
            (board.BUTTON,),
            value_when_pressed=False,
            pull=True,
        )
        self.button_event = keypad.Event()

    ##########################################
    # main handling

    def main_loop(self):
        if self.button.events.get_into(self.button_event):
            if self.button_event.pressed:
                if self.button_event.key_number == 0:
                    print("button 0 pressed.")


    # time.sleep(IMAGE_DELAY)

    def run(self):
        self.print(42 * "*")
        self.print("run")
        # if supervisor.runtime.serial_connected:
        # self.ui.userinput_print_help()
        running = True
        while running:
            try:
                self.main_loop()
            except KeyboardInterrupt as e:
                self.print("KeyboardInterrupt - Stop Program.", e)
                running = False

##########################################
if __name__ == "__main__":
    main = ButtonTest()
    main.run()