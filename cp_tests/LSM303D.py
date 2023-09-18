# SPDX-FileCopyrightText: 2023 s-light Stefan Krüger
# SPDX-License-Identifier: MIT
"""CircuitPython Driver for the LSM303D accelerometer and magnetometer/compass"""

# based on 
# https://forum.pololu.com/t/lsm303d-raspberry-pi-driver/7698
#       Driver by Fayetteville Free Library Robotics Group
#       First follow the procedure to enable I2C on R-Pi.
#       1. Add the lines "ic2-bcm2708" and "i2c-dev" to the file /etc/modules
#       2. Comment out the line "blacklist ic2-bcm2708" (with a #) in the file /etc/modprobe.d/raspi-blacklist.conf
#       3. Install I2C utility (including smbus) with the command "apt-get install python-smbus i2c-tools"
#       4. Connect the I2C device and detect it using the command "i2cdetect -y 1".  It should show up as 1D or 1E (here the variable LSM is set to 1D).
# and
# https://github.com/adafruit/Adafruit_CircuitPython_LSM303_Accel/blob/c161f1a10c9b052627c3b1c2e95db8fce038a77c/adafruit_lsm303_accel.py#L35

import sys
import struct

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import UnaryStruct
from adafruit_register.i2c_bit import RWBit, ROBit
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_struct_array import StructArray

try:
    from typing import Optional, Tuple
    from typing_extensions import Literal
    from busio import I2C
except ImportError:
    pass

import time
import board

import busio
i2c = busio.I2C(board.IO9, board.IO8)

LSM = 0x1d
device = I2CDevice(i2c, LSM)



LSM_WHOAMI = 0b1001001 #Device self-id

def twos_comp_combine(msb, lsb):
    twos_comp = 256*msb + lsb
    if twos_comp >= 32768:
        return twos_comp - 65536
    else:
        return twos_comp

#Control register addresses -- from LSM303D datasheet

CTRL_0 = 0x1F #General settings
CTRL_1 = 0x20 #Turns on accelerometer and configures data rate
CTRL_2 = 0x21 #Self test accelerometer, anti-aliasing accel filter
CTRL_3 = 0x22 #Interrupts
CTRL_4 = 0x23 #Interrupts
CTRL_5 = 0x24 #Turns on temperature sensor
CTRL_6 = 0x25 #Magnetic resolution selection, data rate config
CTRL_7 = 0x26 #Turns on magnetometer and adjusts mode

#Registers holding twos-complemented MSB and LSB of magnetometer readings -- from LSM303D datasheet
MAG_X_LSB = 0x08 # x
MAG_X_MSB = 0x09
MAG_Y_LSB = 0x0A # y
MAG_Y_MSB = 0x0B
MAG_Z_LSB = 0x0C # z
MAG_Z_MSB = 0x0D

#Registers holding twos-complemented MSB and LSB of accelerometer readings -- from LSM303D datasheet
ACC_X_LSB = 0x28 # x
ACC_X_MSB = 0x29
ACC_Y_LSB = 0x2A # y
ACC_Y_MSB = 0x2B
ACC_Z_LSB = 0x2C # z
ACC_Z_MSB = 0x2D

#Registers holding 12-bit right justified, twos-complemented temperature data -- from LSM303D datasheet
TEMP_MSB = 0x05
TEMP_LSB = 0x06


_BUFFER = bytearray(6)


def _read_u8(device: I2CDevice, address: int) -> int:
    print("_read_u8")
    with device as i2c:
        print("setup read")
        _BUFFER[0] = address & 0xFF
        print("write_then_readinto")
        i2c.write_then_readinto(_BUFFER, _BUFFER, out_end=1, in_end=1)
    return _BUFFER[0]

def _write_u8(device: I2CDevice, address: int, val: int) -> None:
    with device as i2c:
        _BUFFER[0] = address & 0xFF
        _BUFFER[1] = val & 0xFF
        i2c.write(_BUFFER, end=2)

def _read_bytes(
    device: I2CDevice, address: int, count: int, buf: bytearray
) -> None:
    with device as i2c:
        buf[0] = address & 0xFF
        i2c.write_then_readinto(buf, buf, out_end=1, in_end=count)






def scann_bus():
    print("scann_bus: ")
    while not i2c.try_lock():
        pass
    try:
        print([hex(x) for x in i2c.scan()])
    finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
        i2c.unlock()


def read_accel():
    with device:
        # device.write(bytes([0x0f]))
        # result = bytearray(2)
        # device.readinto(result)    
        # # print("result: '{0:b}'".format(int.from_bytes(result, byteorder=sys.byteorder)))
        # print("result: bin - ", result)
        # if result == LSM_WHOAMI:
        if _read_u8(device, 0x0f) == LSM_WHOAMI:
            print('LSM303D detected successfully.')
        else:
            print('No LSM303D detected.')

        print('setup sensor..')
        _write_u8(device, CTRL_1, 0b1010111) # enable accelerometer, 50 hz sampling
        _write_u8(device, CTRL_2, 0x00) #set +/- 2g full scale
        _write_u8(device, CTRL_5, 0b01100100) #high resolution mode, thermometer off, 6.25hz ODR
        _write_u8(device, CTRL_6, 0b00100000) # set +/- 4 gauss full scale
        _write_u8(device, CTRL_7, 0x00) #get magnetometer out of low power mode
        print('setup done.')

        magx = twos_comp_combine(_read_u8(device, MAG_X_MSB), _read_u8(device, MAG_X_LSB))
        magy = twos_comp_combine(_read_u8(device, MAG_Y_MSB), _read_u8(device, MAG_Y_LSB))
        magz = twos_comp_combine(_read_u8(device, MAG_Z_MSB), _read_u8(device, MAG_Z_LSB))

        print("Magnetic field (x, y, z):", magx, magy, magz)

        accx = twos_comp_combine(_read_u8(device, ACC_X_MSB), _read_u8(device, ACC_X_LSB))
        accy = twos_comp_combine(_read_u8(device, ACC_Y_MSB), _read_u8(device, ACC_Y_LSB))
        accz = twos_comp_combine(_read_u8(device, ACC_Z_MSB), _read_u8(device, ACC_Z_LSB))

        print("Acceleration (x, y, z):", accx, accy, accz)




# main programm

time.sleep(0.1)
scann_bus()
time.sleep(0.1)

while True:
    read_accel()
    time.sleep(2)


