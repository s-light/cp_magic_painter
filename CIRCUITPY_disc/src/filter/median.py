# median.py : platform-independent median filter
# No copyright, 2020-2021, Garth Zeglin.  This file is explicitly placed in the public domain.
# source: https://courses.ideate.cmu.edu/16-223/f2021/text/code/pico-signals.html#median-py

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
