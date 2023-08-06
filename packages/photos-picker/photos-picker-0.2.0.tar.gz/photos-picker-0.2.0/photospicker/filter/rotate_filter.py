from photospicker.filter.abstract_filter import AbstractFilter
from PIL import ExifTags


class RotateFilter(AbstractFilter):

    def __init__(self, expand=True):
        """
        Constructor

        :param bool expand: wheteher the image will be
            expanded to hold the entire rotated image
        """
        self._expand = expand

    def execute(self, original_img, exif_data):
        """
        Rotate photo according to EXIF data

        :param Image original_img: image object to rotate
        :param dict exif_data    : image exif data

        :return Image
        """
        orientation_key = None
        for key in ExifTags.TAGS.keys():
            if ExifTags.TAGS.get(key) == 'Orientation':
                orientation_key = key

        angle = None
        if exif_data:
            if orientation_key is not None and orientation_key in exif_data:
                if exif_data[orientation_key] == 3:
                    angle = 180
                elif exif_data[orientation_key] == 6:
                    angle = 270
                elif exif_data[orientation_key] == 8:
                    angle = 90

        if angle is None:
            return original_img

        return original_img.rotate(angle, expand=self._expand)
