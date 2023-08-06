"""
Copied from https://docs.python.org/3/howto/logging-cookbook.html#use-of-alternative-formatting-styles
"""


class BraceMessage(object):
    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)
