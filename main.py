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

# add src as import path
import sys
sys.path.append('/src')

import time
import board

from magicpainter import MagicPainter

def wait_with_print(wait_duration = 5, step_duration = 0.25):
    for index in range(wait_duration * step_duration):
        print(".", end="")
        time.sleep(step_duration / wait_duration)

def main():
    """Main handling."""
    wait_with_print(10)
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
