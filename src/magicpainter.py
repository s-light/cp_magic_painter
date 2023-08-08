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

The Software has 4 Modes:
- Lamp
- POV (Persistence Of Vision) 
- LightPainting Picture (TBD)
- LightPainting Point (TBD)


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

import json

from configdict import extend_deep

# import slight_lsm303d_accel

import adafruit_lis3dh

# from adafruit_bno08x import (
#     BNO_REPORT_LINEAR_ACCELERATION,
#     BNO_REPORT_STABILITY_CLASSIFIER,
# )
# from adafruit_bno08x.i2c import BNO08X_I2C

from povpainter import POVPainter
from rgblamp import RGBLamp


import keypad

# button = digitalio.DigitalInOut(board.BUTTON)
# button.switch_to_input(pull=digitalio.Pull.UP)

##########################################
# main class


class MagicPainter(object):
    """MagicPainter."""

    config_defaults = {
        # all sub default parts are defined in the modules themselfes..
    }
    config = {}

    def __init__(self):
        super(MagicPainter, self).__init__()
        # self.print is later replaced by the ui module.
        self.print = lambda *args: print(*args)

        self.print("MagicPainter")
        self.print("  https://github.com/s-light/cp_magic_painter")
        self.print(42 * "*")

        self.load_config()

        self.mode = "lamp"
        self.myPOVPainter = None
        # self.myPOVPainter = POVPainter()
        self.myRGBLamp = RGBLamp()

        self.init_userInput()

        # self.setup_hw()
        # self.setup_modes()
        # self.setup_ui()

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

    # def get_pin(self, bus_name, pin_name):
    #     board_pin_name = self.config["hw"][bus_name][pin_name]
    #     return getattr(board, board_pin_name)

    # def setup_hw(self):
    #     # self.dotstar = busio.SPI(board.IO36, board.IO35)
    #     self.dotstar = busio.SPI(
    #         self.get_pin("dotstar_spi", "clock"), self.get_pin("dotstar_spi", "data")
    #     )
    #     while not self.dotstar.try_lock():
    #         pass
    #     self.dotstar.configure(baudrate=12000000)
    #     # initially set to black
    #     self.dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
    #     for r in range(36 * 5):
    #         self.dotstar.write(bytearray([0xFF, 0x00, 0x00, 0x00]))
    #     self.dotstar.write(bytearray([0xFF, 0xFF, 0xFF, 0xFF]))
    #     # https://docs.circuitpython.org/en/latest/shared-bindings/neopixel_write/index.html
    #     # import neopixel_write
    #     # import digitalio
    #     # pixel_pin = digitalio.DigitalInOut(board.NEOPIXEL)
    #     # pixel_pin.direction = digitalio.Direction.OUTPUT
    #     # neopixel_write.neopixel_write(pixel_pin, bytearray([1, 1, 1]))

    #     # self.i2c = busio.I2C(board.IO9, board.IO8)
    #     # self.i2c = busio.I2C(
    #     #     self.get_pin("accel_i2c", "clock"),
    #     #     self.get_pin("accel_i2c", "data")
    #     # )
    #     # self.accel_sensor = slight_lsm303d_accel.LSM303D_Accel(self.i2c)

    #     # self.i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
    #     # self.bno = BNO08X_I2C(self.i2c)
    #     # self.bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)
    #     # self.bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)

    #     self.i2c = board.I2C()
    #     self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(self.i2c)
    #     self.lis3dh.range = adafruit_lis3dh.RANGE_16_G
    #     self.lis3dh.data_rate = adafruit_lis3dh.DATARATE_LOWPOWER_5KHZ  # → 0,2ms

    # def setup_ui(self):
    #     # self.ui = ui.MagicPainterUI(magicpainter=self)
    #     pass

    def switch_to_next_state(self):
        if self.mode == "lamp":
            self.mode = "magic"
        # elif self.mode == "magic":
        #     self.mode = "lightpainting_image"
        # elif self.mode == "lightpainting_image":
        #     self.mode = "lightpainting_color"
        # elif self.mode == "lightpainting_color":
        #     self.mode = "lamp"
        else:
            self.mode = "lamp"

    ##########################################
    # ui / button handling

    def handle_buttons(self):
        if self.button_event.pressed:
                if self.button_event.key_number == 0:
                    # self.switch_to_next_state()
                    # self.myPOVPainter.switch_image()
                    self.myPOVPainter.switch_image()

    ##########################################
    # main handling

    def main_loop(self):
        if self.button.events.get_into(self.button_event):
            self.handle_buttons()

        if self.mode == "lamp":
            self.myRGBLamp.main_loop()
        elif self.mode == "magic":
            self.myPOVPainter.main_loop()
        # elif self.mode == "lightpainting_image":
        #     self.myPOVPainter.main_loop()


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
