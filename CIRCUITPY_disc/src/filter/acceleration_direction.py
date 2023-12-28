import time
from filter.median import MedianFilter, MedianFilterExtended


def average(input_list):
    return sum(input_list) / len(input_list)


class DirectionChangedEvent(object):
    def __init__(self, *, direction, durations, instance):
        self.direction = direction
        self.durations = durations
        self.instance = instance

    def __str__(self):
        return "'{}' direction: {:+}; durations: {}".format(
            self.instance.axis_name,
            self.direction,
            self.durations,
        )


class AverageBuffer(object):
    def __init__(self, *, buffer_size, stable_threshold=None):
        self.stable_threshold = stable_threshold
        self.buffer_size = buffer_size
        self.buffer = [0] * self.buffer_size
        self.average = 0.1

    def update_input(self, input):
        # remove oldest value
        self.buffer.pop(0)
        # add new
        self.buffer.append(input)

    def update_average(self):
        self.average = average(self.buffer)
        return self.average

    def update(self, input):
        self.update_input(input)
        return self.update_average()

    @property
    def min(self):
        return min(self.buffer)

    @property
    def max(self):
        return max(self.buffer)

    @property
    def max_delta(self):
        return abs(max(self.buffer) - min(self.buffer))

    @property
    def stable(self):
        if self.stable_threshold:
            return self.max_delta < self.stable_threshold
        else:
            return None

    def buffer_as_formatted_string(self, format="{:>4.0f}"):
        template = ", ".join([format] * len(self.buffer))
        template = "[" + template + "]"
        # result = template.format(*self.buffer)
        result = template.format(*[x * 1000 for x in self.buffer])
        return result

    def __getitem__(self, index):
        return self.buffer[index]

    def __len__(self):
        return self.buffer_size

    def __str__(self):
        return "avg {}".format(self.average)


class Durations(object):
    def __init__(self, *, buffer_size, stable_threshold):
        self.buffer_size = buffer_size
        self.stable_threshold = stable_threshold
        self.current_stroke = 0.1
        self.backward_avg = AverageBuffer(
            buffer_size=buffer_size,
            stable_threshold=stable_threshold,
        )
        self.forward_avg = AverageBuffer(
            buffer_size=buffer_size,
            stable_threshold=stable_threshold,
        )

    def __str__(self):
        # return (
        #     "forward {:>4.0f}ms {}; "
        #     "backward {:>4.0f}ms {}; "
        #     "".format(
        #         # iam a bit puzzled.. this should be in ms without the `*1000`
        #         # but this way the values seems correct..
        #         self.forward_avg.average * 1000,
        #         self.forward_avg.buffer_as_formatted_string(),
        #         self.backward_avg.average * 1000,
        #         self.backward_avg.buffer_as_formatted_string(),
        #     )
        # )
        return (
            "forward  {:>4.0f}ms (stable:{:>1}  {:>5.3f}ms  {:>3.2f}Hz); "
            "backward {:>4.0f}ms (stable:{:>1}  {:>5.3f}ms  {:>3.2f}Hz);"
            "".format(
                # iam a bit puzzled.. this should be in ms without the `*1000`
                # but this way the values seems correct..
                self.forward_avg.average * 1000,
                self.forward_avg.stable,
                self.forward_avg.max_delta,
                1 / self.forward_avg.average,

                self.backward_avg.average * 1000,
                self.backward_avg.stable,
                self.backward_avg.max_delta,
                1 / self.backward_avg.average,
            )
        )


class AccelerationDirection(object):
    debug_print_template = (
        "{:5.2f};"  # input_raw,
        "{:+3d}; "  # direction_raw
        "{:1d}; "  # direction_changed
        "{:7.3f}; "  # filter
        "{:7.3f}; "  # filter
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
        noise=1.2,
        buffer_size=4,
        trend_window_split=None,
        callback_direction_changed=None,
        axis_name=None,
    ):
        """
        Special Filter for Direction detection in Acceleration Data.

        Tries to detect a trend / direction in acceleration data.
        based on
        - average filter
        - comparing old & new window in buffer
        """

        self.axis_name = axis_name

        self.buffer_size = buffer_size
        if trend_window_split is None:
            self.trend_window_split = self.buffer_size // 2 - 1
        self.buffer = AverageBuffer(buffer_size=buffer_size)

        self.noise = noise
        self.avg0 = 0.0
        self.avg1 = 0.0
        self.avg2 = 0.0

        # Exponentially Weighted Moving Average
        self.ewma_weight = 0.2
        self.ewma = 0.0
        self.ewma2_weight = 0.1
        self.ewma2 = 0.0

        # self.base_filter = MedianFilterExtended(buffer_size=20, window_size=3)
        # self.base_filter = MedianFilter(window_size=20)

        self.direction_raw = 0
        self.direction_raw_last = 0
        self.direction_changed = False
        self.direction_changed_timestamp = time.monotonic()

        self.durations = Durations(buffer_size=5, stable_threshold=0.040)

        # performance:
        # we create a class global event so we do not recreate and destroy it on every stroke...
        self.direction_changed_event = DirectionChangedEvent(
            direction=self.direction_raw, durations=self.durations, instance=self
        )

        self.callback_direction_changed = callback_direction_changed

    def format_current_value(self):
        return self.debug_print_template.format(
            self.buffer[-1],
            self.direction_raw,
            self.direction_changed,
            self.ewma,
            self.ewma2,
            # self.base
            # *self.filter_buffer,
        )

    def update_avg(self, input_raw):
        self.avg0 = self.buffer.update(input_raw)
        self.avg1 = average(self.buffer[: self.trend_window_split])
        self.avg2 = average(self.buffer[self.trend_window_split :])

    def update_ewma(self):
        # https://hackaday.com/2019/09/06/sensor-filters-for-coders/
        self.ewma = ((1 - self.ewma_weight) * self.ewma) + (
            self.ewma_weight * self.buffer[-1]
        )
        self.ewma2 = ((1 - self.ewma2_weight) * self.ewma2) + (
            self.ewma2_weight * self.ewma
        )

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

            if self.direction_raw != 0:
                # calculate stroke duration
                duration = time.monotonic() - self.direction_changed_timestamp
                self.direction_changed_timestamp = time.monotonic()

                if self.direction_raw == +1:
                    self.durations.current_stroke = self.durations.forward_avg.update(
                        duration
                    )
                elif self.direction_raw == -1:
                    self.durations.current_stroke = self.durations.backward_avg.update(
                        duration
                    )

            if self.callback_direction_changed:
                self.direction_changed_event.direction = self.direction_raw
                self.callback_direction_changed(self.direction_changed_event)

        else:
            self.direction_changed = False

    def update(self, input_raw):
        self.update_avg(input_raw)
        self.update_ewma()
        # self.base = self.base_filter.update(input_raw)

        if input_raw < (self.noise * -1) or input_raw > self.noise:
            self.update_direction()

        return self.direction_changed
