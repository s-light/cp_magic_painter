# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar

"""CircuitPython Essentials DotStar example"""
import time
import adafruit_dotstar
import board

num_pixels = 36
pixels = adafruit_dotstar.DotStar(
    board.SCK,
    board.MOSI,
    # board.D11,
    # board.D10,
    num_pixels,
    brightness=0.2,
    auto_write=False,
)




start = time.monotonic()
time.sleep(1)
print(3 * "\n")
print("DotStar FirstLight")
time.sleep(1.1)
print("runtime: {:0.3f}min".format((time.monotonic() - start) / 60))
while True:
    for i in range(num_pixels):
        pixels.fill((1, 1, 100))
        pixels[i] = (1, 100, 0)
        pixels.show()
        time.sleep(0.1)
    print("runtime: {:0.3f}min".format((time.monotonic() - start) / 60))
