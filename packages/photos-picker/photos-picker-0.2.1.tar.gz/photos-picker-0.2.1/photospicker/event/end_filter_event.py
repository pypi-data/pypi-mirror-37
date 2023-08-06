from photospicker.filter.abstract_filter import AbstractFilter  # noqa


class EndFilterEvent(object):
    """Event dispatched after a filter execution"""

    def __init__(self, photo_filter, filepath):
        """
        Constructor

        :param AbstractFilter photo_filter: filter
        :param str filepath               : file processed by the filter
        """
        self._filter_name = photo_filter.__class__.__name__
        self._filepath = filepath

    def filter_name(self):  # pragma: no cover
        """
        Getter for the filter name

        :return str
        """
        return self._filter_name

    def filepath(self):  # pragma: no cover
        """
        Getter for the file path of the processes file

        :return: str
        """
        return self._filepath
