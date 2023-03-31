import sys
from typing import AnyStr

COLOR_ERROR = "\033[91m"
COLOR_WARNING = "\033[93m"
COLOR_END = "\033[0m"

class ErrorHelper:
    """
    Mixin class for operators to simplify error/warning handling.
    """

    def error(self, msg: AnyStr) -> set:
        """
        Report and print error message.

        :param str msg: The error message
        :return: :code:`{"CANCELLED"}`
        """

        print(f"{COLOR_ERROR}error: {msg}{COLOR_END}", file=sys.stderr)
        self.report({"ERROR"}, msg)
        return {"CANCELLED"}

    def warning(self, msg: AnyStr):
        """
        Report and print warning.

        :param str msg: The warning message
        """

        print(f"{COLOR_WARNING}warning: {msg}{COLOR_END}")
        self.report({"WARNING"}, msg)
