# SPDX-FileCopyrightText: 2023 s-light.eu stefan krüger
# SPDX-License-Identifier: MIT

import time
import board

import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


msg_template = "'{:<10}'  needs {:10.4f}ms/call"
count = 100000


if hasattr(board, "DISPLAY"):
    import displayio

    print("deactivate display..")
    board.DISPLAY.auto_refresh = False
    board.DISPLAY.root_group = displayio.Group()


start = time.monotonic()
for i in range(count):
    led.value = not led.value
end = time.monotonic()
duration = (end - start) / count
duration_ms = duration * 1000
print(msg_template.format("led_blink1", duration_ms))


start = time.monotonic()
for i in range(count):
    led.value = True
    led.value = False
end = time.monotonic()
duration = (end - start) / count
duration_ms = duration * 1000
print(msg_template.format("led_blink2", duration_ms))


if hasattr(board, "DISPLAY"):
    print("activate display..")
    board.DISPLAY.auto_refresh = True
    board.DISPLAY.root_group = displayio.CIRCUITPYTHON_TERMINAL


print("done...")
