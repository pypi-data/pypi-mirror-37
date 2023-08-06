from abc import ABCMeta, abstractmethod
from photospicker.event.scan_progress_event import ScanProgressEvent
from zope import event
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
            excluded_paths=None
    ):
        """
        Constructor

        :param mixed directory_paths: directory paths to scan
        :param int   photos_count:    photos count to pick
        :param list  patterns:        patterns (in lowercase) that files must
                                      match for being scanned
        :param list  excluded_paths:  directory paths excluded form the scan
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

        if excluded_paths is None:
            excluded_paths = []

        self._excluded_paths = []
        for excluded_path in excluded_paths:
            self._excluded_paths.append(os.path.abspath(excluded_path))

    @property
    def picked_file_paths(self):
        """Return an array of the picked file paths"""
        return self._picked_file_paths

    def initialize(self):
        """Fill in the list of files to scan"""
        for path in self._paths:
            for root, dirnames, filenames in os.walk(path):
                if self._is_in_excluded_paths(root):
                    continue
                for filename in filenames:
                    for pattern in self._patterns:
                        if fnmatch.fnmatch(filename.lower(), pattern):
                            self._files_to_scan.append(os.path.join(
                                root,
                                filename
                            ))

    def _is_in_excluded_paths(self, path):
        """
        Check if a path is (or is in) an excluded path

        :param string path: path to check

        :return: bool
        """
        for excluded_path in self._excluded_paths:
            if string.find(path, excluded_path) == 0:
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
