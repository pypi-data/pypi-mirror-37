from abc import ABCMeta, abstractmethod
import os


class AbstractUploader:
    """Abstract class for creating "upload" classes"""

    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor"""
        self._photo_counter = 0

    def initialize(self):  # pragma: no cover
        """Initialize method which can be used by subclasses"""
        pass

    @abstractmethod
    def upload(self, binary, original_filename):  # pragma: no cover
        """
        Upload or copy files to destination

        :param str binary           : binary data to upload
        :param str original_filename: original file name

        :raise NotImplementedError
        """
        raise NotImplementedError()

    def increase_photo_counter(self):
        """Increase photo counter"""
        self._photo_counter += 1

    def _build_filename(self, original_filename):
        """
        Return next photo to upload filename

        :param str original_filename: name of the original file

        :return str
        """
        filename, ext = os.path.splitext(original_filename)
        return 'photo{counter}{ext}'.format(
            counter=self._photo_counter,
            ext=ext.lower()
        )
