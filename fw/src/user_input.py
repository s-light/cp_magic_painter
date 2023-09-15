# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

import time

import board
import touchio
import keypad
from adafruit_debouncer import Debouncer

from configdict import extend_deep


class UserInput(object):
    """UserInput."""

    config_defaults = {
        "hw": {
            "touch": {
                "pins": [
                    board.D5,
                    board.D6,
                    board.D7,
                ],
                "threshold": 4000,
            },
        },
    }

    def __init__(self, *, config, callback_button, callback_touch):
        super(UserInput, self).__init__()

        print("init UserInput..")

        self.config = config
        extend_deep(self.config, self.config_defaults.copy())

        self.callback_button = callback_button
        self.callback_touch = callback_touch

        self.init_userInput()

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

        self.touch_pins = []
        self.touch_pins_debounced = []
        for touch_id,touch_pin in enumerate(self.config["hw"]["touch"]["pins"]):
            touch = touchio.TouchIn(touch_pin)
            # reset default threshold
            threshold = self.config["hw"]["touch"]["threshold"]
            print(
                "["
                # +"{:>9} → "
                "{:>2}] "
                "touch.raw_value ({}) + threshold {} = {}".format(
                    # str(touch_pin),
                    touch_id,
                    touch.raw_value,
                    threshold,
                    touch.raw_value + threshold,
                )
            )
            touch.threshold = touch.raw_value + threshold
            self.touch_pins.append(touch)
            self.touch_pins_debounced.append(Debouncer(touch))

    def touch_print_status(self):
        for index, touch in enumerate(self.touch_pins):
            print(
                "{:>2}: {:>5} - {:>7}"
                "".format(
                    index,
                    touch.value,
                    touch.raw_value,
                ),
                end=""
            )
        print()

    def update(self):
        if self.button.events.get_into(self.button_event):
            if self.button_event.pressed:
                if self.button_event.key_number == 0:
                    self.callback_button()
        for touch_id, touch_debounced in enumerate(self.touch_pins_debounced):
            touch_debounced.update()
            if touch_debounced.fell or touch_debounced.rose or touch_debounced.value:
                self.callback_touch(touch_id, touch_debounced)
        # debugoutput
        # self.touch_print_status()

    def run_test(self):
        print(42 * "*")
        print("test...")
        running = True
        while running:
            try:
                self.update()
                self.touch_print_status()
                time.sleep(0.2)
            except KeyboardInterrupt as e:
                print("KeyboardInterrupt - Stop Program.", e)
                running = False

def dev_test():
    
    import sys
    sys.path.append("/src")
    # import user_input 

    def cb_button():
        print("button pressed!")

    def cb_touch(touch_debounced):
        print("touch_debounced activated!")

    ui = UserInput(
        config={},
        callback_button=cb_button,
        callback_touch=cb_touch,
    )
    ui.run_test()

if __name__ == "__main__":
    dev_test()
