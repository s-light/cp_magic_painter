#!/usr/bin/env python3
# coding=utf-8
# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
CircuitPython Essentials Storage CP Filesystem boot.py file
"""
import time
import board
import digitalio
import storage
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

# Turn the NeoPixel white for one second to indicate when to press the boot button.
pixel.fill((255, 255, 255))
time.sleep(1)

# default:
default = "circuitpython_readonly"
# == computer writeable
# default = "circuitpython_writeable"
# == computer readonly

# button PUSHED = 0 = False = connected to ground
if default is "circuitpython_readonly":
    # button pushed == circuitpython_readonly: True
    # button clear  == circuitpython_readonly: False
    circuitpython_readonly = not button.value
else:
    # button pushed == circuitpython_readonly: False
    # button clear  == circuitpython_readonly: True
    circuitpython_readonly = button.value




print("set cp filesystem to:")
if circuitpython_readonly:
    print(" → writeable for computer - readonly by CircuitPython")
    pixel.fill((0, 255, 100))
else:
    print(" → readonly for computer - writeable by CircuitPython")
    pixel.fill((255, 0, 200))
    import storage
    storage.disable_usb_drive()

# mount this from the cp point of view
storage.remount("/", readonly=circuitpython_readonly)

time.sleep(1)
pixel.fill((0, 1, 0))


# deactivate display.
print("deactivate display backlight.")
board.DISPLAY.brightness = 0



# USB things...
# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/circuitpy-midi-serial

# → → not enough endpoints  available for ESP32-S3 :-(

# import usb_cdc
# import usb_midi

# print("boot.py: usb_mindi disable")
# usb_midi.disable()
# print("boot.py: usb_cdc enable console & data")
# usb_cdc.enable(console=True, data=True)


# if not circuitpython_readonly:
#     import storage
#     print("boot.py: disable usb_drive")
#     storage.disable_usb_drive()
#     import usb_cdc
#     print("boot.py: usb_cdc enable console & data")
#     usb_cdc.enable(console=True, data=True)