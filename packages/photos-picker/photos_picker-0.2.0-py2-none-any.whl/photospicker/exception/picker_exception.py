from exceptions import BaseException


class PickerException(BaseException):
    """Exception when picking photos"""

    # Error constants
    NOT_FOUND = 1
    NOT_EMPTY = 2

    def __init__(self, code, message):
        """
        Constructor

        :param int code   : error code
        :param str message: error message
        """
        self._code = code
        self._message = message

    @property
    def code(self):  # pragma no cover
        """
        Getter code

        :return int
        """
        return self._code

    @property
    def message(self):  # pragma no cover
        """
        Getter message

        :return str
        """
        return self._message
