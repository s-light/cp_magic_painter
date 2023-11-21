import board

from adafruit_fancyled.adafruit_fancyled import CHSV, CRGB

config = {
    # in wich mode to start: (RGBLamp | POVPainter)
    "start_mode": "RGBLamp",
    "hw": {
        "touch": {
            "pins": [
                # board.D5,
                # board.D6,
                # board.D7,
            ],
            # "threshold": 4000,
        },
        "accel_i2c_pins": {
            "clock": "SCL",
            "data": "SDA",
        },
    },
    # "data": {},
    "rgblamp": {
        # "mode": "nightlight",
        "brightness": 0.02,
        # effect duration in seconds
        "effect_duration": 10 * 60,
        # https://learn.adafruit.com/fancyled-library-for-circuitpython/colors#hsv-colors-2981215
        # only specifying Hue → purple
        # "color_range": {
        #     "min": CHSV(0.50),
        #     "max": CHSV(0.9),
        # },
        # warm orange
        "color_range": {
            "min": CHSV(0.08),
            "max": CHSV(0.12),
        },
    },
}
