from timeit import default_timer
from typing import AnyStr

COLOR_DEBUG = "\033[96m"
COLOR_END = "\033[0m"

class Timer:
    """
    Context manager for timing code snippets.

    :param str name: if specified, print it together with the elapsed time when exiting the
        context
    :ivar time: elapsed time (only available after exiting the context)
    :vartype time: float
    """

    def __init__(self, name: AnyStr = None):
        self._name = name

    def __enter__(self):
        self._start = default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        self.time = default_timer() - self._start
        if self._name is not None:
            print(f"{COLOR_DEBUG}{_auto_format_duration(self.time)} [{self._name}]{COLOR_END}")

def _auto_format_duration(time_s: float):
    if (us := time_s * 1e6) < 1e4:
        return f"{us:7.2f} us"
    elif (ms := time_s * 1e3) < 1e4:
        return f"{ms:7.2f} ms"
    else:
        return f"{time_s:7.2f} s "
