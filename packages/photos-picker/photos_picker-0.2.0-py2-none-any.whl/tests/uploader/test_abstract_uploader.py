from unittest import TestCase
from photospicker.uploader.abstract_uploader import AbstractUploader


class DummyUploader(AbstractUploader):
    """Dummy class for testing AbstractUploader"""
    def upload(self, binary, original_filename):
        """Dummy abstract method"""
        pass

    def build_filename(self, original_filename):
        """
        Wrapper for private method _build_filename

        :param str original_filename: name of the original file

        :return str
        """
        return self._build_filename(original_filename)


class TestAbstractUploader(TestCase):
    """Test class for AbstractUploader"""

    def test_build_filename(self):
        """Test filename built"""
        uploader = DummyUploader()
        uploader.increase_photo_counter()
        filename = uploader.build_filename('myphoto1.JPG')
        self.assertEqual('photo1.jpg', filename)
        uploader.increase_photo_counter()
        filename = uploader.build_filename('myphoto27.png')
        self.assertEqual('photo2.png', filename)
