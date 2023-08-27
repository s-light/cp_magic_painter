#!/usr/bin/env python3
# coding=utf-8

"""
collection of some small helper functions
"""

import time

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


def map_range_constrained(x, in_min, in_max, out_min, out_max):
    """Map value from one range to another - constrain input range."""
    if x < in_min:
        x = in_min
    elif x > in_max:
        x = in_max
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_to_01(x, in_min, in_max):
    """Map value to 0..1 range."""
    return (x - in_min) / (in_max - in_min)

def map_01_to(x, out_min, out_max):
    """Map value from 0..1 to given range."""
    return x * (out_max - out_min) / 1.0 + out_min


def map_to_11(x, in_min, in_max):
    """Map value to -1..1 range."""
    return (x - in_min) * 2 / (in_max - in_min) + -1


def map_range_int(x, in_min, in_max, out_min, out_max):
    """Map value from one range to another."""
    return int(
        (x - in_min) * (out_max - out_min)
        //
        (in_max - in_min) + out_min
    )


def map_range_constrained_int(x, in_min, in_max, out_min, out_max):
    """Map value from one range to another - constrain input range."""
    if x < in_min:
        x = in_min
    elif x > in_max:
        x = in_max
    return int(
        (x - in_min) * (out_max - out_min)
        //
        (in_max - in_min) + out_min
    )


def wait_with_print(duration=1):
    """Wait with print."""
    step_duration = 0.5
    start = time.monotonic()
    last_print = time.monotonic()
    while (time.monotonic() - start) < duration:
        if (time.monotonic() - last_print) >= step_duration:
            # print(". ", end='', flush=True)
            print(".", end='')
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
