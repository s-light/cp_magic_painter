import board

from adafruit_fancyled.adafruit_fancyled import CHSV, CRGB

config = {
    "hw": {
        "touch": {
            "pins": [
                board.D6,
                board.D5,
                board.D7,
            ],
            # "threshold": 4000,
        },
    },
    # "data": {},
    "rgblamp": {
        # "mode": "nightlight",
        "brightness": 0.02,
        # https://learn.adafruit.com/fancyled-library-for-circuitpython/colors#hsv-colors-2981215
        # "base_color": CHSV(0.7),  # only specifiing Hue. purple
    },
}
