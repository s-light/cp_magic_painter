#!/usr/bin/env python3
# coding=utf-8

"""
Magic Painter
based on 
https://learn.adafruit.com/circuitpython-painter
https://learn.adafruit.com/clue-light-paintstick    

HW: some high speed processor...
tested with ESP32-S3
"""


# import os
import time
import sys
import board
import digitalio
from magicpainter import MagicPainter
from rgblamp import RGBLamp

button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

##########################################
# globals

##########################################


def main():
    """Main handling."""
    wait_duration = 5
    step_duration = 0.25
    for index in range(wait_duration * step_duration):
        print(".", end="")
        time.sleep(step_duration / wait_duration)
    print("")
    print(42 * "*")
    print("Python Version: " + sys.version)
    print("board: " + board.board_id)
    print(42 * "*")
    myMagicPainter = MagicPainter()
    myMagicPainter.run()


##########################################
if __name__ == "__main__":
    main()

##########################################
