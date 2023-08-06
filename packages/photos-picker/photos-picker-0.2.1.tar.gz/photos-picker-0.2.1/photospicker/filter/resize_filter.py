from photospicker.filter.abstract_filter import AbstractFilter
from PIL import Image


class ResizeFilter(AbstractFilter):
    """Resize a photo"""

    def __init__(self, max_width, max_height):
        """
        Constructor

        :param int max_width : max width after filter execution
        :param int max_height: max height after filter execution
        """
        self._width = max_width
        self._height = max_height

    def execute(self, original_img, exif_data):
        """
        Resize photo

        :param Image original_img: image object to resize
        :param dict exif_data    : image exif data

        :return Image
        """
        (original_width, original_height) = original_img.size

        diff_wh = self._width - self._height
        sign_diff_wh = diff_wh / abs(diff_wh)
        diff_original_wh = original_width - original_height
        sign_diff_original_wh = diff_original_wh / abs(diff_original_wh)

        if sign_diff_wh == sign_diff_original_wh:
            w = self._width
            h = self._height
        else:
            w = self._height
            h = self._width

        if original_width / original_height > w / h:
            ratio = float(w) / original_width
        else:
            ratio = float(h) / original_height

        resized_img = original_img.resize(
            (int(ratio * original_width), int(ratio * original_height)),
            Image.ANTIALIAS
        )

        return resized_img
