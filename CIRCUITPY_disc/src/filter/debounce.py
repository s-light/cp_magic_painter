# debounce.py : platform-independent median filter
# No copyright, 2020-2021, Garth Zeglin.  This file is explicitly placed in the public domain.
# source: https://courses.ideate.cmu.edu/16-223/f2021/text/code/pico-signals.html#hysteresis-py

class Debounce:
    def __init__(self, samples=5):
        """Filter to 'debounce' an integer stream by suppressing changes from the previous value
        until a specific new value has been observed a minimum number of times."""

        self.samples = samples          # number of samples required to change        
        self.current_value = 0          # current stable value
        self.new_value = None           # possible new value        
        self.count = 0                  # count of new values observed

    def update(self, input):
        if input == self.current_value:
            # if the input is unchanged, keep the counter at zero            
            self.count = 0
            self.new_value = None
        else:
            if input != self.new_value:
                # start a new count
                self.new_value = input
                self.count = 1
            else:
                # count repeated changes
                self.count += 1
                if self.count >= self.samples:
                    # switch state after a sufficient number of changes
                    self.current_value = self.new_value
                    self.count = 0
                    self.new_value = None
                    
        return self.current_value