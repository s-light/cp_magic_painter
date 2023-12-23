# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT
# source https://github.com/s-light/cp_magic_painter/


"""
# Magic Painter - POV Zauberstab
based on & inspired by
https://learn.adafruit.com/circuitpython-painter
https://learn.adafruit.com/clue-light-paintstick


## HW: 
- Adafruit QT Py ESP32-S3 https://www.adafruit.com/product/5426
- Adafruit LIS3DH breakout https://www.adafruit.com/product/2809
- APA102 (Dotstar) Pixel-LED-Strip

## Usage

The Software has 2 Modes:
- Lamp
- POV (Persistence Of Vision) 


"""

# this file is the main entry point
# and handles the User-Interface and the prepares the sub-parts.


##########################################
# imports

# import os
import sys


import gc
import time

import board
import busio
import digitalio

import touchio
from adafruit_debouncer import Debouncer

import keypad

# import slight_lsm303d_accel

import adafruit_lis3dh

# from adafruit_bno08x import (
#     BNO_REPORT_LINEAR_ACCELERATION,
#     BNO_REPORT_STABILITY_CLASSIFIER,
# )
# from adafruit_bno08x.i2c import BNO08X_I2C

from config_base import ConfigBaseClass
from povpainter import POVPainter
from rgblamp import RGBLamp
from user_input import UserInput

import config as config_file

# button = digitalio.DigitalInOut(board.BUTTON)
# button.switch_to_input(pull=digitalio.Pull.UP)

##########################################
# main class


class MagicPainter(ConfigBaseClass):
    """MagicPainter."""

    config_defaults = {
        # all sub default parts are defined in the modules themselfes..
        "test": 42,
        "start_mode":"rgblamp",
    }
    config = {}

    def __init__(self):
        super(MagicPainter, self).__init__(config={})
        # self.print is later replaced by the ui module.
        # self.print = lambda *args: print(*args)
        # self.print("MagicPainter")

        print(8 * "\n")
        print(42 * "*")
        print("MagicPainter")
        print("  https://github.com/s-light/cp_magic_painter")
        print(42 * "*")

        # self.config = self.load_config_from_file()
        self.config = config_file.config
        self.config_extend_with_defaults(defaults=self.config_defaults)
        # print(self.__class__, "config extended:")
        # self.config_print()

        self.userinput = UserInput(
            config=self.config,
            callback_button=self.switch_to_next_mode,
            callback_touch=self.handle_touch,
            callback_gesture=self.handle_gesture,
        )

        self.modes = [
            RGBLamp(
                config=self.config,
                accel_sensor=self.userinput.accel_sensor,
            ),
            POVPainter(
                config=self.config,
                accel_sensor=self.userinput.accel_sensor,
            ),
        ]
        self.mode = self.modes[0]
        if "POV" in self.config["start_mode"]:
            self.mode = self.modes[1]

        # print(2 * "\n")
        # print(42 * "*")
        # print("loaded and extended config:")
        # self.config_print()
        # print(2 * "\n")

        self.mode.spi_init()

    # def setup_ui(self):
    #     # self.ui = ui.MagicPainterUI(magicpainter=self)
    #     pass

    ##########################################
    # ui / button handling

    def switch_to_next_mode(self):
        mode_index = self.modes.index(self.mode)
        mode_index += 1
        if mode_index >= len(self.modes):
            mode_index = 0

        print("current mode ", self.mode.__qualname__)
        self.mode.spi_deinit()
        print("spi_deinit done.")
        self.mode = self.modes[mode_index]
        print("switched mode to ", self.mode.__qualname__)
        self.mode.spi_init()
        print("spi_init done.")

    def handle_touch(self, event):
        self.mode.handle_user_input(event)
    
    def handle_gesture(self, event):
        self.mode.handle_gesture(event)

    ##########################################
    # main handling

    def main_loop(self):
        self.userinput.update()
        # if supervisor.runtime.serial_bytes_available:
        #     self.check_input()
        self.mode.main_loop()
        # Small delay to keep things responsive but give time for interrupt processing.
        time.sleep(0)

    def run(self):
        print(42 * "*")
        print("run")
        # if supervisor.runtime.serial_connected:
        # self.ui.userinput_print_help()
        running = True
        while running:
            try:
                self.main_loop()
            except KeyboardInterrupt as e:
                print("KeyboardInterrupt - Stop Program.", e)
                running = False
