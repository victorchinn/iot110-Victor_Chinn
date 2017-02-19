SHIFT_MASK = 15
class Debouncer(object):
    """Shift Register Debouncer"""

    def __init__(self):
        self.switch_shift_register = 0

    # perform AND logic debouncer
    def debounce(self, switch_in):
        self.switch_shift_register = (self.switch_shift_register << 1) | switch_in
        return int((self.switch_shift_register & SHIFT_MASK) == SHIFT_MASK)
