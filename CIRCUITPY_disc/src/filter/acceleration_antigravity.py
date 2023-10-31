import time
from filter.median import MedianFilter, MedianFilterExtended


def average(input_list):
    return sum(input_list) / len(input_list)


class AccelerationAntigravity(object):
    debug_print_template = (
        "{:1d}; "  # rest_active
        # X
        "{:7.3f}; "
        "{:7.3f}; "
        "{:7.3f}; "
        # Y
        "{:7.3f}; "
        "{:7.3f}; "
        "{:7.3f}; "
        # Z
        "{:7.3f}; "
        "{:7.3f}; "
        "{:7.3f}; "
        # sum
        "{:7.3f}; "
    )

    def __init__(
        self,
        *,
        min_duration_in_rest=0.3,
        gravity_threshold=1.5,
    ):
        """
        Special Filter to remove Acceleration Data Gravity Offsets.

        """
        self.gravity_threshold = gravity_threshold
        self.min_duration_in_rest = min_duration_in_rest
        self.sum = 0
        self.input_raw = (0, 0, 0)
        self.base = (0, 0, 0)
        self.input_corrected = (0, 0, 0)
        self.rest_debounce = False
        self.rest_active = False
        self.rest_start_timestamp = time.time()

    def format_current_value(self):
        return self.debug_print_template.format(
            self.rest_active,
            self.input_raw[0],
            self.base[0],
            self.input_corrected[0],
            self.input_raw[1],
            self.base[1],
            self.input_corrected[1],
            self.input_raw[2],
            self.base[2],
            self.input_corrected[2],
            self.sum,
        )

    def update(self, input_raw):
        self.input_raw = input_raw
        # self.sum = sum(input_raw)
        
        self.sum = abs(input_raw[0]) + abs(input_raw[1]) + abs(input_raw[2])
        if self.sum <= self.gravity_threshold:
            if self.rest_debounce:
                current_rest_duration = time.time() - self.rest_start_timestamp
                if current_rest_duration >= self.min_duration_in_rest:
                    self.rest_active = True
                    self.base = self.input_raw
                    # we are in rest position.
                    # not moving..
                    # so we assume that the current values are the base levels of these axis.
                    # this way we removing any gravity offset..
                else:
                    self.rest_active = False
            else:
                # transition from moving to rest
                self.rest_debounce = True
                self.rest_active = False
                self.rest_start_timestamp = time.time()
        else:
            self.rest_debounce = False
            self.rest_active = False
            self.rest_start_timestamp = time.time()

        # https://stackoverflow.com/a/11677882/574981
        # self.input_corrected = [
        #     in_value - base_value
        #     for in_value, base_value in zip(self.base, self.input_raw)
        # ]
        self.input_corrected = (
            self.input_raw[0] - self.base[0],
            self.input_raw[1] - self.base[1],
            self.input_raw[2] - self.base[2],
        )
        return self.input_corrected
