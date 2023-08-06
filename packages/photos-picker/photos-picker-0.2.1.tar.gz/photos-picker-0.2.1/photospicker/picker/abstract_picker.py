from abc import ABCMeta, abstractmethod
from photospicker.event.scan_progress_event import ScanProgressEvent
from zope import event
from photospicker.exception.picker_exception import PickerException
import os
import fnmatch
import string


class AbstractPicker:
    """
    Abstract class for creating "picker" classes

    A picker object select files in a path according to a strategy
    which characterizes the picker
    """

    __metaclass__ = ABCMeta

    def __init__(
            self,
            directory_paths,
            photos_count,
            patterns=None,
            excluded_patterns=None
    ):
        """
        Constructor

        :param mixed directory_paths:   directory paths to scan
        :param int   photos_count:      photos count to pick
        :param list  patterns:          patterns (in lowercase) that files must
                                        match for being scanned
        :param list  excluded_patterns: directory patterns excluded
                                        form the scan
        :raise TypeError
        """
        if isinstance(directory_paths, list):
            self._paths = directory_paths
        else:
            self._paths = [directory_paths]

        self._files_to_scan = []
        self._picked_file_paths = []
        self._photos_count = photos_count

        if patterns is None:
            patterns = ['*.tif', '*.tiff', '*.jpg', '*.jpeg', '*.png']
        elif not isinstance(patterns, list):
            raise TypeError("patterns argument must be a list")

        self._patterns = patterns

        if excluded_patterns is None:
            self._excluded_patterns = []
        else:
            self._excluded_patterns = excluded_patterns

    @property
    def picked_file_paths(self):
        """Return an array of the picked file paths"""
        return self._picked_file_paths

    def initialize(self):
        """Fill in the list of files to scan"""
        for path in self._paths:
            for root, dirnames, filenames in os.walk(path):
                if self._is_in_excluded_patterns(root):
                    continue
                for filename in filenames:
                    for pattern in self._patterns:
                        if fnmatch.fnmatch(filename.lower(), pattern):
                            self._files_to_scan.append(os.path.join(
                                root,
                                filename
                            ))
        if not self._files_to_scan:
            raise PickerException(
                PickerException.EMPTY_SCAN,
                "No photos to scan found in given directory(ies)"
            )

    def _is_in_excluded_patterns(self, path):
        """
        Check if a path match with an excluded pattern

        :param string path: path to check

        :return: bool
        """
        for excluded_pattern in self._excluded_patterns:
            if string.find(path + '/', excluded_pattern) != -1:
                return True
        return False

    @abstractmethod
    def scan(self):  # pragma: no cover
        """
        Scan the given path for building picked file paths list

        :raise NotImplementedError
        """
        raise NotImplementedError()

    def _notify_progress(self, scanned):
        """
        Notify the progress state of the scan

        :param int scanned: scanned files count
        """
        event.notify(ScanProgressEvent(
            scanned,
            len(self._files_to_scan),
            False
        ))

    def _notify_end(self):
        """Notify the end of the scan"""
        to_scan = len(self._files_to_scan)
        event.notify(ScanProgressEvent(to_scan, to_scan, True))
