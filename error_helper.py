from typing import AnyStr

from _error_helper import error, warning

COLOR_ERROR = "\033[91m"
COLOR_WARNING = "\033[93m"
COLOR_END = "\033[0m"

class ErrorHelper:
    """
    Mixin class for operators to simplify error/warning handling.
    """

    def error(self, msg: AnyStr, prefix="error: ") -> set:
        """
        Report and print error message.

        :param str msg: The error message
        :return: :code:`{"CANCELLED"}`
        """

        error(msg, prefix=prefix)
        self.report({"ERROR"}, msg)
        return {"CANCELLED"}

    def warning(self, msg: AnyStr, prefix="warning: "):
        """
        Report and print warning.

        :param str msg: The warning message
        """

        warning(msg, prefix=prefix)
        self.report({"WARNING"}, msg)
