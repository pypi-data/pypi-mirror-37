class ScanProgressEvent(object):
    """Event dispatched during scan and holding progress data"""

    def __init__(self, files_scanned, files_to_scan, end):
        """
        Constructor

        :param int files_scanned: files scanned count
        :param int files_to_scan: total files count to scan
        :param bool end         : whether the scan is ended
        """
        self._files_scanned = files_scanned
        self._files_to_scan = files_to_scan
        self._end = end

    @property
    def files_scanned(self):  # pragma: no cover
        """
        Getter for the scanned files count

        :return int
        """
        return self._files_scanned

    @property
    def files_to_scan(self):  # pragma: no cover
        """
        Getter for the total files count to scan

        :return int
        """
        return self._files_to_scan

    @property
    def end(self):  # pragma: no cover
        """
        Getter for whether the scan is ended

        :return bool
        """
        return self._end
