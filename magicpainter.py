# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
#
# SPDX-License-Identifier: MIT

# original CircuitPython Painter:
# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Dotstar painter! Can handle up to ~2300 pixel size image (e.g. 36 x 64)


"""
Magic Painter - POV Zauberstab
based on https://learn.adafruit.com/circuitpython-painter


HW: some high speed processor...
tested with ESP32-S3
"""


##########################################
# imports


import gc
import time

import board
import busio
import digitalio

import json

from configdict import extend_deep

# import slight_lsm303d_accel

from adafruit_bno08x import (
    BNO_REPORT_LINEAR_ACCELERATION,
    BNO_REPORT_STABILITY_CLASSIFIER,
)
from adafruit_bno08x.i2c import BNO08X_I2C

##########################################
# main class


class MagicPainter(object):
    """MagicPainter."""

    config_defaults = {
        # ItsiBitsy M4
        "hw": {
            "dotstar_spi": {
                "clock": "SCK",
                "data": "MOSI",
            },
            "accel_i2c": {
                "clock": "SCL",
                "data": "SDA",
            },
        },
        # ESP32-S3
        # "hw": {
        #     "dotstar_spi": {
        #         "clock": "D4",
        #         "data": "D12",
        #     },
        #     "accel_i2c": {
        #         "clock": "D8",
        #         "data": "D9",
        #     },
        # },
        # all sub defaults for the UI are defined there.
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

        self.filename = "blinka.bmp"
        self.brightness = 0.3
        self.PIXEL_DELAY = 0.003

        # we'll resize this later
        self.image_buffer = bytearray(0)
        self.bmpHeight = 0
        self.bmpWidth = 0

        self.setup_hw()
        # self.setup_modes()
        # self.setup_ui()

        # self.load_image_to_buffer(self.filename, self.self.image_buffer)
        self.load_image(self.filename)

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

    def get_pin(self, bus_name, pin_name):
        board_pin_name = self.config["hw"][bus_name][pin_name]
        return getattr(board, board_pin_name)

    def setup_hw(self):
        # self.dotstar = busio.SPI(board.IO36, board.IO35)
        self.dotstar = busio.SPI(
            self.get_pin("dotstar_spi", "clock"), self.get_pin("dotstar_spi", "data")
        )
        while not self.dotstar.try_lock():
            pass
        self.dotstar.configure(baudrate=12000000)

        # https://docs.circuitpython.org/en/latest/shared-bindings/neopixel_write/index.html
        # import neopixel_write
        # import digitalio
        # pixel_pin = digitalio.DigitalInOut(board.NEOPIXEL)
        # pixel_pin.direction = digitalio.Direction.OUTPUT
        # neopixel_write.neopixel_write(pixel_pin, bytearray([1, 1, 1]))

        # self.i2c = busio.I2C(board.IO9, board.IO8)
        # self.i2c = busio.I2C(
        #     self.get_pin("accel_i2c", "clock"),
        #     self.get_pin("accel_i2c", "data")
        # )
        # self.accel_sensor = slight_lsm303d_accel.LSM303D_Accel(self.i2c)

        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
        self.bno = BNO08X_I2C(self.i2c)
        self.bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)
        self.bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)

    def setup_ui(self):
        # self.ui = ui.MagicPainterUI(magicpainter=self)
        pass

    # def load_image_to_buffer(self, filename, self.image_buffer):
    def load_image(self, filename):
        try:
            with open("/" + filename, "rb") as f:
                print("File opened")
                if f.read(2) != b"BM":  # check signature
                    raise BMPError("Not BitMap file")

                bmpFileSize = read_le(f.read(4))
                f.read(4)  # Read & ignore creator bytes

                bmpImageoffset = read_le(f.read(4))  # Start of image data
                headerSize = read_le(f.read(4))
                self.bmpWidth = read_le(f.read(4))
                self.bmpHeight = read_le(f.read(4))
                flip = True

                print(
                    "Size: %d\nImage offset: %d\nHeader size: %d"
                    % (bmpFileSize, bmpImageoffset, headerSize)
                )
                print("Width: %d\nHeight: %d" % (self.bmpWidth, self.bmpHeight))

                if read_le(f.read(2)) != 1:
                    raise BMPError("Not singleplane")
                bmpDepth = read_le(f.read(2))  # bits per pixel
                print("Bit depth: %d" % (bmpDepth))
                if bmpDepth != 24:
                    raise BMPError("Not 24-bit")
                if read_le(f.read(2)) != 0:
                    raise BMPError("Compressed file")

                print("Image OK!")

                rowSize = (self.bmpWidth * 3 + 3) & ~3  # 32-bit line boundary

                # its huge! but its also fast :)
                self.image_buffer = bytearray(self.bmpWidth * self.bmpHeight * 4)

                for row in range(self.bmpHeight):  # For each scanline...
                    if flip:  # Bitmap is stored bottom-to-top order (normal BMP)
                        pos = bmpImageoffset + (self.bmpHeight - 1 - row) * rowSize
                    else:  # Bitmap is stored top-to-bottom
                        pos = bmpImageoffset + row * rowSize

                    # print ("seek to %d" % pos)
                    f.seek(pos)
                    for col in range(self.bmpWidth):
                        b, g, r = bytearray(f.read(3))  # BMP files store RGB in BGR
                        # front load brightness, gamma and reordering here!
                        order = [b, g, r]
                        idx = (col * self.bmpHeight + (self.bmpHeight - row - 1)) * 4
                        self.image_buffer[idx] = 0xFF  # first byte is 'brightness'
                        idx += 1
                        for color in order:
                            self.image_buffer[idx] = int(
                                pow((color * self.brightness) / 255, 2.7) * 255 + 0.5
                            )
                            idx += 1

        except OSError as e:
            if e.args[0] == 28:
                raise OSError("OS Error 28 0.25")
            else:
                raise OSError("OS Error 0.5")
        except BMPError as e:
            print("Failed to parse BMP: " + e.args[0])

        gc.collect()
        print(gc.mem_free())
        print("Ready to go!")

    ##########################################
    # helper

    ##########################################
    # system mode

    # def switch_to_mode(self, mode):
    #     """switch to new mode."""
    #     pass

    ##########################################
    # draw image

    def draw(self, backwards=False):
        # print("Draw!")
        index = 0
        bmp_range = range(self.bmpWidth)
        if backwards:
            bmp_range = range(self.bmpWidth, -1)
        for col in bmp_range:
            row = self.image_buffer[index : index + self.bmpHeight * 4]
            self.dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
            self.dotstar.write(row)
            self.dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
            index += self.bmpHeight * 4
            time.sleep(self.PIXEL_DELAY)

        # clear it out
        self.dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
        for r in range(self.bmpHeight * 5):
            self.dotstar.write(bytearray([0xFF, 0x00, 0x00, 0x00]))
        self.dotstar.write(bytearray([0xFF, 0xFF, 0xFF, 0xFF]))
        gc.collect()

    ##########################################
    # main handling

    def main_loop(self):
        gc.collect()
        # self.mode_current.update()
        # self.ui.update()
        # self.check_buttons()
        # if supervisor.runtime.serial_bytes_available:
        #     self.check_input()
        # accel_x, accel_y, accel_z = self.accel_sensor._raw_acceleration
        (
            accel_x,
            accel_y,
            accel_z,
        ) = self.bno.linear_acceleration  # pylint:disable=no-member
        # print(
        #     "X: {: > 10.6f}  Y: {: > 10.6f} Z: {: > 10.6f}  m/s^2  ({})".format(
        #         accel_x,
        #         accel_y,
        #         accel_z,
        #         self.bno.stability_classification,
        #     )
        # )
        print(
            "{: > 10}, {: > 10.6f}".format(
                time.monotonic(),
                accel_y,
            )
        )

        if accel_y > 7:
            # neopixel_write.neopixel_write(pixel_pin, bytearray([255, 0, 0]))
            self.draw(backwards=True)
        elif accel_y < -7:
            # neopixel_write.neopixel_write(pixel_pin, bytearray([0, 0, 255]))
            self.draw()

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


def read_le(s):
    # as of this writting, int.from_bytes does not have LE support, DIY!
    result = 0
    shift = 0
    for byte in bytearray(s):
        result += byte << shift
        shift += 8
    return result


class BMPError(Exception):
    pass
