from photospicker.exception.abstract_exception import AbstractException


class PickerException(AbstractException):
    """Exception when picking photos"""

    # Error constants
    EMPTY_SCAN = 1
