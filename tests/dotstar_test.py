# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar

"""CircuitPython Essentials DotStar example"""
import time
from rainbowio import colorwheel
import adafruit_dotstar
import board

num_pixels = 36
pixels = adafruit_dotstar.DotStar(
    # board.SCK,
    # board.MOSI,
    board.D11,
    board.D10,
    num_pixels,
    brightness=1,
    auto_write=False,
)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // (num_pixels * 3)) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


print(3 * "\n")
print("DotStar Rainbow")
while True:
    rainbow_cycle(0.4)
    print(time)
