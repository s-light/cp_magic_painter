#!/usr/bin/env python3
# coding=utf-8

"""
Minimal partly recursive prettyprint.
"""

def pretty_print(*, container={}, line_pre=""):
    """Minimal partly recursive prettyprint."""
    print(
        "{}{{".format(
            line_pre,
        )
    )
    _pretty_print(container=container, line_pre=line_pre + (4 * " "))
    print(
        "{}}}".format(
            line_pre,
        )
    )

def _pretty_print(*, container=None, line_pre=""):
    """Minimal partly recursive prettyprint."""
    for name, value in container.items():
        # print(name, type(value))
        if (type(value) is dict):
            print(
                "{}{}: {{".format(
                    line_pre,
                    name,
                )
            )
            _pretty_print(
                container=value,
                line_pre=line_pre + (4 * " "),
            )
            print(
                "{}}},".format(
                    line_pre,
                )
            )
        elif (type(value) is list):
            print(
                "{}{}: [".format(
                    line_pre,
                    name,
                )
            )
            for item in value:
                print("{}{},".format(line_pre + (4 * " "), repr(item)))
            print(
                "{}],".format(
                    line_pre,
                )
            )
        elif (type(value) is tuple):
            print(
                "{}{}: (".format(
                    line_pre,
                    name,
                )
            )
            for item in value:
                print("{}{},".format(line_pre + (4 * " "), repr(item)))
            print(
                "{}),".format(
                    line_pre,
                )
            )
        else:
            print("{}{}: {},".format(line_pre, name, repr(value)))
