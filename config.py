import board

config = {
    "hw": {
        "touch": {
            "pins": [
                board.D5,
                board.D6,
                board.D7,
            ],
            "threshold": 4000,
        },
        "dotstar_spi": {
            "clock": "SCK",
            "data": "MOSI",
        },
        "accel_i2c": {
            "clock": "SCL1",
            "data": "SDA1",
        },
    }
}
