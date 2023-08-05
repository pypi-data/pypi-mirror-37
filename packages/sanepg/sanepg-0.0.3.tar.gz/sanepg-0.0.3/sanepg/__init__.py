
# a generic error class for throwing exceptions
class SaneError(Exception):
    def __init__(self, fmt, *args):
        self.message = fmt % args

    def __str__(self):
        return self.message

from .pool import connect
