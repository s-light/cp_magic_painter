#!/usr/bin/env python3
# coding=utf-8

"""
setup
"""


import usb_cdc

# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/circuitpy-midi-serial
print("usb_cdc: enable console & data")
usb_cdc.enable(console=True, data=True)
