# POV Painter - POV Zauberstab
# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT
# source https://github.com/s-light/cp_magic_painter/
#
# based on
#
# CircuitPython Painter
#     SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#     SPDX-License-Identifier: MIT
#     source: https://learn.adafruit.com/circuitpython-painter
#
# CLUE lightpainting
#     SPDX-FileCopyrightText: 2020 Phillip Burgess for Adafruit Industries
#     SPDX-License-Identifier: MIT
#     source: https://learn.adafruit.com/clue-light-paintstick/code-with-circuitpython


"""
POV Painter - POV Zauberstab

based on 
    CircuitPython Painter
        https://learn.adafruit.com/circuitpython-painter
    CLUE lightpainting 
        https://learn.adafruit.com/clue-light-paintstick/code-with-circuitpython


HW: some high speed processor...
    - QT Py ESP32-S3
    - Lis3dh
    - dotstar / APA102 compatible led strip
"""


##########################################
# imports


import gc
import time

import board
import busio
import digitalio
import displayio

import json

import adafruit_imageload
import ansi_escape_code as terminal
from ansi_escape_code.progressbar import ProgressBar

from mode_base import ModeBaseClass

from configdict import extend_deep

import helper

from bmp2led import BMP2LED, BMPError

from gesture_detector import DIRECTION_CHANGED

##########################################
# main class


class POVPainter(ModeBaseClass):
    """POVPainter."""

    config_defaults = {
        # QT Py ESP32-S3
        "data": {
            "paint_mode_classic": True,
            "image_folder": "/images",
            "temp_file": "/led.dat",
            "led_data_file_benchmark": "/led_benchmark.dat",
            # Correction for perceptually linear brightness
            "gamma": 2.4,
            # Min, max brightness (0.0-1.0)
            "brightness_range": (0.15, 0.75),
            # draw / stroke duration in seconds
            # "times": ["1/8", "1/4", "1/3", "1/2", "2/3", "1", "1.5", "2", "3", "4"],
            "draw_duration": 0.7,
        },
    }

    def __init__(self, *, config={}, accel_sensor):
        super(POVPainter, self).__init__(config=config)
        print(42 * "*")
        print("POVPainter")
        print("  https://github.com/s-light/cp_magic_painter")
        print(42 * "*")

        self.config_extend_with_defaults(defaults=self.config_defaults)
        # print(self.__class__, "config extended:")
        # self.config_print()

        self.accel_sensor = accel_sensor

        # prepare internals
        self.spi_init_done = False
        self.first_run = False
        self._brightness = None

        self.pixel_count = self.config["hw"]["pixel_count"]

        self.paint_mode_classic = self.config["data"]["paint_mode_classic"]
        if self.paint_mode_classic:
            self.load_image = self.load_image_v1
            self.paint = self.paint_v1
        else:
            self.load_image = self.load_image_v2
            self.paint = self.paint_v2

        self.fs_writeable = self.check_filesystem_writeable()
        print("fs_writeable ", self.fs_writeable)

        # OLD Draw version = classic
        self.pixel_delay = 0.0014
        self.pixel_delay_max = 0.0016
        # self.pixel_delay = 0.0

        self.image_buffer = bytearray(0)
        self.bmpHeight = 0
        self.bmpWidth = 0

        # Advanced CLUE version
        self.bmp2led = BMP2LED(
            pixel_count=self.pixel_count,
            color_order=self.config["hw"]["pixel_color_order"],
            gamma=self.config["data"]["gamma"],
        )
        self.path = self.config["data"]["image_folder"]
        self.tempfile = self.config["data"]["temp_file"]
        self.led_data_file_benchmark = self.config["data"]["led_data_file_benchmark"]
        self.brightness_range = self.config["data"]["brightness_range"]

        # self.times = self.config["data"]["times"]
        # self.times.sort(key=eval)  # Ensure times are shortest-to-longest
        self.draw_duration = self.config["data"]["draw_duration"]

        # TODO: try https://github.com/adafruit/Adafruit_CircuitPython_DotStar/blob/main/examples/dotstar_image_pov.py
        # Get list of compatible BMP images in path
        self.images = self.bmp2led.scandir(self.path)
        if not self.images:
            print("no images found. using testpattern.")
            # TODO implement / generate test-pattern
            # https://docs.circuitpython.org/projects/display-shapes/en/latest/api.html#adafruit_display_shapes.rect.Rect
            # https://learn.adafruit.com/circuitpython-display-support-using-displayio/library-overview
            # https://docs.circuitpython.org/en/latest/shared-bindings/bitmaptools/index.html#bitmaptools.draw_line
        else:
            print("found images at '" + self.path + "':")
            for img in self.images:
                print("  ", img)

        self.image_num = 0  # Current selected image index in self.path
        self.filename = self.path + "/" + self.images[self.image_num]

        self.num_rows = 0  # Nothing loaded yet
        self.loop = False  # Repeat image playback
        self.brightness = 0.2  # LED brightness, 0.0 (off) to 1.0 (bright)
        self.config_mode = 0  # Current setting being changed
        self.rect = None  # Multipurpose     progress/setting rect
        # self.time = (len(self.times) + 1) // 2  # default to center of range

        self.setup_hw()

        # only setup things..
        self.rows_per_second = -1
        self.row_size = -1

        # start pixel...
        self.spi_init()

        # next time spi_init is called we will do benchmark and image loading..
        self.first_run = True

        self.spi_deinit()

    ##########################################
    # properties

    @property
    def brightness(self):
        # return super(ModeBaseClass, self).brightness * 2
        return ModeBaseClass.brightness

    @brightness.setter
    def brightness(self, value):
        # super(POVPainter, self).brightness = value
        # https://github.com/python/cpython/issues/59170#issuecomment-1093581234
        # we need a workaround..
        # ModeBaseClass.brightness=value

        # value = helper.limit(value, 0.0, 1.0)
        # self._brightness = value

        # Remap brightness from 0.0-1.0 to brightness_range.
        ModeBaseClass.brightness = helper.map_01_to(
            value,
            self.brightness_range[0],
            self.brightness_range[1],
        )
        if self.spi_init_done:
            self.load_image()

    ##########################################
    # sub system init

    def first_run_init(self):
        # Determine filesystem-to-LEDs throughput (also clears LED strip)
        self.rows_per_second, self.row_size = self.benchmark()
        self.clear_strip()
        print(
            "rows_per_second: {}, row_size: {}".format(
                self.rows_per_second,
                self.row_size,
            )
        )

        self.load_image()

    def spi_init(self):
        # deactivate internal displays...
        displayio.release_displays()
        self.dotstar = busio.SPI(
            clock=helper.get_pin(
                config=self.config, bus_name="pixel_spi_pins", pin_name="clock"
            ),
            MOSI=helper.get_pin(
                config=self.config, bus_name="pixel_spi_pins", pin_name="data"
            ),
        )
        while not self.dotstar.try_lock():
            pass
        self.dotstar.configure(baudrate=12000000)
        # initially set to black
        self.dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
        for r in range(36 * 5):
            self.dotstar.write(bytearray([0xFF, 0x00, 0x00, 0x00]))
        self.dotstar.write(bytearray([0xFF, 0xFF, 0xFF, 0xFF]))

        if self.first_run:
            self.first_run_init()
            self.first_run = False

        self.spi_init_done = True

    def spi_deinit(self):
        self.dotstar.deinit()
        self.spi_init_done = False

    def setup_hw(self):
        # self.dotstar = busio.SPI(board.IO36, board.IO35)
        # https://docs.circuitpython.org/en/latest/shared-bindings/neopixel_write/index.html
        # import neopixel_write
        # import digitalio
        # pixel_pin = digitalio.DigitalInOut(board.NEOPIXEL)
        # pixel_pin.direction = digitalio.Direction.OUTPUT
        # neopixel_write.neopixel_write(pixel_pin, bytearray([1, 1, 1]))
        pass

    def setup_ui(self):
        # self.ui = ui.POVPainterUI(magicpainter=self)
        pass

    ##########################################
    # helper

    def check_filesystem_writeable(self):
        """
        check if filesystem is writeable.
        """
        writeable = False
        try:
            with open("writeable.test", "wb") as file:
                writeable = True
        except OSError as error:
            #  error.args[0] == 28:  # If the file system is full...
            if error.errno == 30:
                # Read-only filesystem
                print(error)
                writeable = False
            else:
                print(error)
                raise error
        return writeable

    ##########################################
    # dotstar helper

    def dotstar_set_pixel(self, *, begin, end, r, g, b):
        """
        Set range of dotstar pixel to color.
        """
        pixel_count = self.bmp2led.pixel_count
        begin = helper.limit(begin, 0, pixel_count - 1)
        end = helper.limit(end, 0, pixel_count - 1)
        pixel_on_count = (end - begin) + 1
        pixel_off_end_count = (pixel_count - 1) - end

        off_pixel = [255, 0, 0, 0]
        on_pixel = [255, 0, 0, 0]
        on_pixel[1 + self.bmp2led.red_index] = r
        on_pixel[1 + self.bmp2led.green_index] = g
        on_pixel[1 + self.bmp2led.blue_index] = b

        buffer = bytearray(
            # header
            [0] * 4
            # pixel data
            + off_pixel * begin
            + on_pixel * pixel_on_count
            + off_pixel * pixel_off_end_count
            # + off_pixel
            # tail
            + [255] * ((pixel_count + 15) // 16)
        )
        self.dotstar.write(buffer)

    def clear_strip(self):
        """
        Turn off all LEDs of the DotStar strip.
        """
        self.dotstar.write(
            bytearray(
                [0] * 4
                + [255, 0, 0, 0] * self.bmp2led.pixel_count
                + [255] * ((self.bmp2led.pixel_count + 15) // 16)
            )
        )

    def load_progress(self, amount):
        """
        Callback function for image loading, moves progress bar on display.
        Arguments:
            amount (float) : Current 'amount loaded' coefficient; 0.0 to 1.0
        """
        # self.rect.x = int(board.DISPLAY.width * (amount - 1.0))
        # self.terminal_progressbar.update(amount)
        num_on = int(amount * self.bmp2led.pixel_count + 0.5)
        self.dotstar_set_pixel(begin=0, end=num_on, r=0, g=1, b=0)
        # num_off = self.bmp2led.pixel_count - num_on
        # off_pixel = [255, 0, 0, 0]
        # on_pixel = [255, 0, 0, 0]
        # on_pixel[1 + self.bmp2led.green_index] = 1
        # self.dotstar.write(
        #     bytearray(
        #         [0] * 4
        #         + on_pixel * num_on
        #         + off_pixel * num_off
        #         + [255] * ((self.bmp2led.pixel_count + 15) // 16)
        #     )
        # )

    def dotstar_blink(self, blink_count=5, duration=1, r=1, g=0, b=0):
        blink_duration = duration / (blink_count * 2)
        for blink in range(blink_count):
            self.dotstar_set_pixel(begin=0, end=2, r=r, g=g, b=b)
            time.sleep(blink_duration)
            self.clear_strip()
            time.sleep(blink_duration)

    ##########################################
    # load and draw v1

    # def load_image_v1_to_buffer(self, filename, self.image_buffer):
    def load_image_v1(self, filename=None):
        """
        Load image into buffer.

        Arguments:
            filename (string) : full filename (inkl. path) to load.
        """
        if filename is None:
            filename = self.filename
        print("load_image_v1: \n" "    file: '{}'\n" "".format(filename))
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
                print("loading...\n")
                # currently the ProgressBar crashes CP if not connected to the computer..
                # no idea why.. so for now - just do not use it..
                # maybe it is a memory overflow thing?!
                # TODO: add issue
                # self.terminal_progressbar = ProgressBar()
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
                    self.load_progress(row / (self.bmpHeight - 1))

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
        print("load_image_v1 " "('{}') " "done.\n" "".format(filename))
        self.clear_strip()

    def paint_v1(self, backwards=False):
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
            time.sleep(self.pixel_delay)

        # clear it out
        self.dotstar.write(bytearray([0x00, 0x00, 0x00, 0x00]))
        for r in range(self.bmpHeight * 5):
            self.dotstar.write(bytearray([0xFF, 0x00, 0x00, 0x00]))
        self.dotstar.write(bytearray([0xFF, 0xFF, 0xFF, 0xFF]))
        gc.collect()

    ##########################################
    # CLUE V2 version
    def benchmark(self):
        """
        Estimate filesystem-to-LED-strip throughput.
        Returns: rows-per-second throughput (int), LED row size in bytes
        (including DotStar header and footer) (int).
        """

        # Generate a small temporary file equal to one full LED row,
        # all set 'off'.
        row_data = bytearray(
            [0] * 4
            + [255, 0, 0, 0] * self.bmp2led.pixel_count
            + [255] * ((self.bmp2led.pixel_count + 15) // 16)
        )
        row_size = len(row_data)

        if self.fs_writeable:
            try:
                with open(self.led_data_file_benchmark, "wb") as file:
                    file.write(row_data)
            except OSError as error:
                if error.errno == 30:
                    # Read-only filesystem
                    print(error)
                else:
                    raise error

        # For a period of 1 second, repeatedly seek to start of file,
        # read row of data and write to LED strip as fast as possible.
        # Not super precise, but good-enough guess of light painting speed.
        # (Bonus, this will turn off LED strip on startup).
        rows = 0
        with open(self.led_data_file_benchmark, "rb") as file:
            start_time = time.monotonic()
            while time.monotonic() - start_time < 1.0:
                file.seek(0)
                file.readinto(row_data)
                self.dotstar.write(row_data)
                time.sleep(0.001)  # See notes in paint()
                rows += 1

        return rows, row_size

    def load_image_v2(self, filename=None):
        if filename is None:
            filename = self.filename
        """
        Load BMP from image list, determined by variable self.image_num
        (not a passed argument). Data is converted and placed in
        self.tempfile.
        """
        print("loading...\n")

        if self.fs_writeable:
            # pylint: disable=eval-used
            # (It's cool, is a 'trusted string' in the code / config)
            # Playback time in seconds
            # duration = eval(self.times[self.time])

            # The 0.9 here is an empirical guesstimate; playback is ever-so-
            # slightly slower than benchmark speed due to button testing.
            # rows = int(duration * self.rows_per_second * 0.9 + 0.5)
            rows = int(self.draw_duration * self.rows_per_second * 0.9 + 0.5)

            image_filename = self.path + "/" + self.images[self.image_num]
            try:
                self.num_rows = self.bmp2led.process(
                    image_filename,
                    self.tempfile,
                    rows,
                    self.brightness,
                    self.loop,
                    self.load_progress,
                )
            except (MemoryError, BMPError):
                print("TOO BIG")
                self.dotstar_blink()
                time.sleep(4)

            print("Done.")
            self.clear_strip()  # LEDs off
        else:
            print("filesystem ReadOnly. we can only use old led_data files..")
            self.dotstar_blink(blink_count=5, duration=1, r=1, g=0, b=1)

    def paint_v2(self):
        """
        Paint Image once.
        """

        painting = True
        row = 0

        with open(self.tempfile, "rb") as file:
            led_buffer = bytearray(self.row_size)
            # During painting, automatic garbage collection is disabled
            # so there are no pauses in the LED output (which would wreck
            # the photo). This requires that the loop below is written in
            # such a way to avoid ANY allocations within that scope!
            gc.collect()
            gc.disable()

            while painting:
                file.seek(row * self.row_size)
                # using readinto() instead of read() is another
                # avoid-automatic-garbage-collection strategy.
                file.readinto(led_buffer)
                self.dotstar.write(led_buffer)
                # Strip updates are more than fast enough...
                # it's the file conversion that takes forever.
                # This small delay (also present in the benchmark()
                # function) reduces the output resolution slightly,
                # in turn reducing the preprocessing requirements.
                # time.sleep(0.001)
                # TODO Stefan: check this mode!
                # maybe this is not true for pov application?
                row += 1
                if row >= self.num_rows:
                    painting = False

            # Re-enable automatic garbage collection
            gc.enable()

            self.clear_strip()

    ##########################################
    # V3 dotstar_image_pov.py
    # https://github.com/adafruit/Adafruit_CircuitPython_DotStar/blob/main/examples/dotstar_image_pov.py

    ##########################################
    # ui

    def handle_user_input(self, event):
        if event.touch.rose:
            print("POVPainter - handle_user_input: ", event.touch_id)
            # if touch_id == 0:
            #     self.switch_image()
            # if touch_id == 0:
            #     print("brightness ++")
            #     self.brightness += 0.1
            # elif touch_id == 1:
            #     print("brightness --")
            #     self.brightness -= 0.1
            # elif touch_id == 2:
            # if touch_id == 2:
            #     self.switch_image()
        # pass

    def handle_gesture(self, event):
        if event.gesture == DIRECTION_CHANGED:
            #     time.sleep(0.09)
            duration = event.orig_event.durations.current_stroke
            pixel_delay_new = (duration - 0.001) / self.pixel_count
            # print(event)
            print(pixel_delay_new)
            if pixel_delay_new < self.pixel_delay_max:
                self.pixel_delay = pixel_delay_new
            self.paint()

    def switch_image(self):
        """
        Switch to next image.
        """
        self.image_num += 1
        if self.image_num >= len(self.images):
            self.image_num = 0

        self.filename = self.path + "/" + self.images[self.image_num]

        self.load_image(self.filename)

    ##########################################
    # main handling

    def main_loop(self):
        gc.collect()
        # accel_y = self.accel_sensor.acceleration[1]
        # accel_x, accel_y, accel_z = self.accel_sensor.acceleration
        # if accel_y > 10:
        #     # neopixel_write.neopixel_write(pixel_pin, bytearray([255, 0, 0]))
        #     # self.draw(backwards=True)
        #     # self.draw(backwards=True)
        #     # self.draw(backwards=True)
        #     pass
        # elif accel_y < -20:
        #     print(accel_y)
        #     time.sleep(0.09)
        #     # neopixel_write.neopixel_write(pixel_pin, bytearray([0, 0, 255]))
        #     self.paint()

        # if accel_z > 20:
        #     self.switch_image()
        #     time.sleep(5)

        # print(
        #     "{:7.3f}; {:7.3f}; {:7.3f};    "
        #     "".format(
        #         # time.monotonic(),
        #         accel_x,
        #         accel_y,
        #         accel_z,
        #     )
        # )

    # time.sleep(IMAGE_DELAY)

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


##########################################


def read_le(s):
    # as of this writing, int.from_bytes does not have LE support, DIY!
    result = 0
    shift = 0
    for byte in bytearray(s):
        result += byte << shift
        shift += 8
    return result


class BMPError(Exception):
    pass


if __name__ == "__main__":
    print("povpainter.py direct mode.")
