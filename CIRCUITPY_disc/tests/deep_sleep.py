# https://learn.adafruit.com/deep-sleep-with-circuitpython/alarms-and-sleep#pinalarm-deep-sleep-3081649

import alarm
import board
import digitalio
import neopixel
import time


np_power = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
np_power.switch_to_output(value=False)

i2c_power = digitalio.DigitalInOut(board.TFT_I2C_POWER)
i2c_power.switch_to_output(value=False)

np = neopixel.NeoPixel(board.NEOPIXEL, 1)

np[0] = (50, 50, 50)
time.sleep(5)



# prepare sleep
np[0] = (0, 0, 1)
time.sleep(1)
np_power.value = False
i2c_power.value = False

pin_alarm = alarm.pin.PinAlarm(pin=board.D0, value=False, pull=True)

# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(pin_alarm)

# Does not return, so we never get here.