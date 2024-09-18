#!/usr/bin/env python3
# coding=utf-8

"""
collection of some small helper functions
"""

import time
import board


def get_pin(*, config, bus_name, pin_name):
        board_pin_name = config["hw"][bus_name][pin_name]
        return getattr(board, board_pin_name)

def limit(value, value_min, value_max):
    return max(min(value_max, value), value_min)


def round_up(value, round_to=10):
    """round up to next `round_to` value.
    based on: https://stackoverflow.com/a/14092788/574981
    """
    return value + (-value) % round_to


def round_nearest(value, multiple_of):
    """round to `multiple_of` value.
    based on: https://stackoverflow.com/a/28425782/574981
    """
    return round(value / multiple_of) * multiple_of


def map_range(x, in_min, in_max, out_min, out_max):
    """Map value from one range to another."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(x, in_min, in_max):
    """constrain range."""
    if x < in_min:
        x = in_min
    elif x > in_max:
        x = in_max
    return x

def map_range_constrained(x, in_min, in_max, out_min, out_max):
    """Map value from one range to another - constrain input range."""
    x = constrain(x, in_min, in_max)
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_to_01(x, in_min, in_max):
    """Map value to 0..1 range."""
    return (x - in_min) / (in_max - in_min)

def map_to_01_constrained(x, in_min, in_max):
    """Map value to 0..1 range."""
    x = constrain(x, in_min, in_max)
    return map_to_01(x, in_min, in_max)


def map_01_to(x, out_min, out_max):
    """Map value from 0..1 to given range."""
    return x * (out_max - out_min) / 1.0 + out_min

def map_01_to_constrained(x, out_min, out_max):
    """Map value from 0..1 to given range."""
    print("x", x)
    print("out_min", out_min)
    print("out_max", out_max)
    x = map_01_to(x, out_min, out_max)
    print("x", x)
    x = constrain(x, out_min, out_max)
    print("x", x)
    return x


def map_to_11(x, in_min, in_max):
    """Map value to -1..1 range."""
    return (x - in_min) * 2 / (in_max - in_min) + -1


def map_range_int(x, in_min, in_max, out_min, out_max):
    """Map value from one range to another."""
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)


def map_range_constrained_int(x, in_min, in_max, out_min, out_max):
    """Map value from one range to another - constrain input range."""
    if x < in_min:
        x = in_min
    elif x > in_max:
        x = in_max
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)


# multi map


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MultiMap / multi_map


def multi_map(value, map_array):
    """
    Map value with help of in,out tuple array.
    
    loosely based on http:#arduino.cc/playground/Main/MultiMap
    """
    # take care the value is within range
    # val = constrain(val, _in[0], _in[N-1]);
    if (value <= map_array[0][0]):
        return map_array[0][1]

    if (value >= map_array[-1][0]):
        return map_array[-1][1]

    # search right interval
    pos = 1  # map_array[0][0] already tested
    while value > map_array[pos][0]:
        pos += 1

    # this will handle all exact "points" in the array
    if (value == map_array[pos][0]):
        return map_array[pos][1]

    # interpolate in the right segment for the rest
    return map_range(value, map_array[pos - 1][0], map_array[pos][0], map_array[pos - 1][1], map_array[pos][1])


# others


def wait_with_print(duration=1):
    """Wait with print."""
    step_duration = 0.5
    start = time.monotonic()
    last_print = time.monotonic()
    while (time.monotonic() - start) < duration:
        if (time.monotonic() - last_print) >= step_duration:
            # print(". ", end='', flush=True)
            print(".", end="")
            last_print = time.monotonic()
    print("")


def time_measurement_call(message, test_function, loop_count=1000):
    """Measure timing."""
    duration = 0
    start_time = time.monotonic()
    for _index in range(loop_count):
        start_time = time.monotonic()
        test_function()
        end_time = time.monotonic()
        duration += end_time - start_time
    print(
        "{call_duration:>8.2f}ms\t{message}"
        "".format(
            call_duration=(duration / loop_count) * 1000,
            message=message,
        )
    )
