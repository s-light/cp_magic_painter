import time


def average(input_list):
    return sum(input_list) / len(input_list)


class AccelerationDirection(object):

    debug_print_template = (
        "{: 1d}; "  # direction_raw
        "{:7.3f};"  # input_raw,
        "{:7.3f}; "  # self.direction_changed,
        # "avg1:{:7.3f} "
        # "avg2:{:7.3f};     "
        # "{:7.3f}; " # *self.filter_buffer,
        # "["
        # + ("{:7.3f}, " * filter_size)
        # + "]    "
    )

    def __init__(
        self,
        *,
        noise=1.0,
        buffer_size=4,
        trend_window_split=None,
        callback_direction_changed=None,
    ):
        """
        Special Filter for Direction detection in Acceleration Data.

        Tries to detect a trend / direction in acceleration data.
        based on
        - average filter
        - comparing old & new window in buffer
        """
        self.buffer_size = buffer_size
        if trend_window_split is None:
            self.trend_window_split = self.buffer_size // 2 - 1
        self.buffer = [0] * self.buffer_size

        self.noise = noise
        self.avg1 = 0
        self.avg2 = 0

        self.direction_raw = 0
        self.direction_raw_last = 0
        self.direction_changed = False

        self.callback_direction_changed = callback_direction_changed

    def format_current_value(self):
        return self.debug_print_template.format(
            self.direction_raw,
            self.buffer[-1],
            self.direction_changed,
            # *self.filter_buffer,
        )

    def update_buffer(self, input):
        # remove oldest value
        self.buffer.pop(0)
        # add new
        self.buffer.append(input)

    def update_average(self):
        self.avg1 = average(self.buffer[: self.trend_window_split])
        self.avg2 = average(self.buffer[self.trend_window_split :])

    def update_direction(self):
        # detect shake
        if (self.avg1) < self.avg2:
            self.direction_raw = +1
        elif (self.avg1) > self.avg2:
            self.direction_raw = -1
        else:
            self.direction_raw = 0

        if (
            self.direction_raw_last is not self.direction_raw
            and self.direction_raw is not 0
        ):
            self.direction_raw_last = self.direction_raw
            # event! we change
            self.direction_changed = True
            if self.callback_direction_changed:
                self.callback_direction_changed()

        else:
            self.direction_changed = False

    def update(self, input_raw):
        self.update_buffer(input_raw)
        self.update_average()

        if input_raw < (self.noise * -1) or input_raw > self.noise:
            self.update_direction()

        return self.direction_changed
