# median.py : platform-independent median filter
# No copyright, 2020-2021, Garth Zeglin.  This file is explicitly placed in the public domain.
# source: https://courses.ideate.cmu.edu/16-223/f2021/text/code/pico-signals.html#median-py

def median_average(input_list, window_size=0.5):
    sorted_list = input_list.sort()
    window_size_el_count = len(sorted_list) * window_size
    window_start = window_size_el_count
    window_end = len(sorted_list) - window_size_el_count
    return average(sorted_list[window_start:window_end])


class MedianFilter:
    def __init__(self, window_size=5):
        """Non-linear filter to reduce signal outliers by returning the median value
        of the recent history.  The window size determines how many samples
        are held in memory.  An input change is typically delayed by half the
        window width.  This filter is useful for throwing away isolated
        outliers, especially glitches out of range.
        """
        self.window_size = window_size
        self.ring = [0] * window_size     # ring buffer for recent time history
        self.oldest = 0                   # index of oldest sample

    def update(self, input):
        # save the new sample by overwriting the oldest sample
        self.ring[self.oldest] = input
        self.oldest += 1
        if self.oldest >= self.window_size:
            self.oldest = 0
    
        # create a new sorted array from the ring buffer values
        in_order = sorted(self.ring)

        # return the value in the middle
        return in_order[self.window_size//2]

class MedianFilterExtended:
    def __init__(self, buffer_size = 10, window_size=5):
        """Non-linear filter to reduce signal outliers by returning the median value
        of the recent history.  The window size determines how many samples
        are held in memory.  An input change is typically delayed by half the
        window width.  This filter is useful for throwing away isolated
        outliers, especially glitches out of range.
        """
        self.buffer_size = int(buffer_size)
        self.window_size = int(window_size)
        self.ring = [0] * buffer_size     # ring buffer for recent time history
        self.oldest = 0                   # index of oldest sample

        border_size = int((self.buffer_size - self.window_size) / 2)
        self.window_start = border_size
        self.window_end = border_size + self.window_size

    def update(self, input):
        # save the new sample by overwriting the oldest sample
        self.ring[self.oldest] = input
        self.oldest += 1
        if self.oldest >= self.buffer_size:
            self.oldest = 0
    
        # create a new sorted array from the ring buffer values
        in_order = sorted(self.ring)

        # return the value in the middle
        return in_order[self.window_start:self.window_end]
