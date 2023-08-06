from abc import ABCMeta, abstractmethod
from PIL import Image  # noqa


class AbstractFilter:
    """Abstract class for creating filters"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, img, exif_data):  # pragma: no cover
        """
        Execute filter

        :param Image img     : image object to modify
        :param dict exif_data: image exif data

        :return Image
        """
        raise NotImplementedError()
