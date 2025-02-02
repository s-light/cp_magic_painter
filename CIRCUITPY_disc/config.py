import board

from adafruit_fancyled.adafruit_fancyled import CHSV, CRGB

config = {
    # in wich mode to start: (RGBLamp | POVPainter)
    "start_mode": "RGBLamp",
    # "start_mode": "POVPainter",
    "POVPainter": {"brightness": 0.5},
    # light painting
    # "RGBLamp": {
    #     "brightness": 1.0,
    #     # effect duration in seconds
    #     "effect_duration": 15,
    #     "effect_active": True,
    #     # purple
    #     "color_range": {
    #         "min": CHSV(0.50),
    #         "max": CHSV(0.9),
    #     },
    #     "extra_effects": {
    #         "y_to_brightness": False,
    #     },
    # },
    "RGBLamp": {
        "brightness": 0.3,
        # effect duration in seconds
        "effect_duration": 3 * 60,
        "effect_active": True,
        #
        # colors
        # https://learn.adafruit.com/fancyled-library-for-circuitpython/colors#hsv-colors-2981215
        # only specifying Hue for fully saturated color..
        # purple
        # "color_range": {
        #     "min": CHSV(0.50),
        #     "max": CHSV(0.9),
        # },
        # warm orange
        "color_range": {
            "min": CHSV(0.08),
            "max": CHSV(0.14),
        },
        # extra effects...
        "extra_effects": {
            # y_to_brightness can be used for a *candle like* effect
            "y_to_brightness": False,
            # "y_to_brightness": (0.3, 0.7),
        },
    },
    "hw": {
        "pixel_color_order": "bgr",
        "pixel_count": 144,
        "pixel_spi_pins": {
            "clock": "D11",
            "data": "D12",
        },
        "accel_i2c_pins": {
            "clock": "SCL",
            "data": "SDA",
        },
    },
}
