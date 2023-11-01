import board

from adafruit_fancyled.adafruit_fancyled import CHSV, CRGB

config = {
    # in wich mode to start: (RGBLamp | POVPainter)
    "start_mode":"RGBLamp",
    "hw": {
        "touch": {
            "pins": [
                board.D5,
                board.D6,
                board.D7,
            ],
            # "threshold": 4000,
        },
    },
    # "data": {},
    "rgblamp": {
        # "mode": "nightlight",
        "brightness": 0.52,
        # effect duration in seconds
        "effect_duration": 10 * 60, 
        # https://learn.adafruit.com/fancyled-library-for-circuitpython/colors#hsv-colors-2981215
        "base_color": CHSV(0.75),  # only specifying Hue. purple
        # "base_color": CHSV(0.05),  # only specifying Hue. orange
    },
}
