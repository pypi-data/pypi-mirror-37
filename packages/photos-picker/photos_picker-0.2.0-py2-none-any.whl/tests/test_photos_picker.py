from unittest import TestCase
from mock import Mock
from mock import MagicMock
from photospicker.photos_picker import PhotosPicker
from callee.types import InstanceOf
from io import BytesIO
import mock


class TestPhotosPicker(TestCase):
    """Test the main photos picker class"""

    @staticmethod
    def _filter_execute_side_effect(file_content):
        """
        Side effect for filter execute method

        :param str file_content: binary content of the file

        :return: str
        """
        return file_content

    @mock.patch('__builtin__.open')
    def test_run_without_filters(self, mock_open):
        """
        Test run method without filters

        :param MagicMock mock_open: open built'in function mock
        """

        open_mock1 = MagicMock()
        open_mock1.__enter__().read.return_value = 'mydata1'

        open_mock2 = MagicMock()
        open_mock2.__enter__().read.return_value = 'mydata2'

        mock_open.side_effect = [open_mock1, open_mock2]

        picker = Mock()
        picker.picked_file_paths = [
            '/myfolder/myphoto1.jpg',
            '/myfolder/myphoto2.png'
        ]

        uploader = Mock()

        photos_picker = PhotosPicker(picker, (), uploader)
        photos_picker.run()

        picker.initialize.assert_called_once()
        picker.scan.assert_called_once()

        mock_open.assert_has_calls([
            mock.call('/myfolder/myphoto1.jpg', mode='rb'),
            mock.call('/myfolder/myphoto2.png', mode='rb')
        ])

        open_mock1.__enter__().read.assert_called_once()
        open_mock2.__enter__().read.assert_called_once()

        uploader.initialize.assert_called_once()
        uploader.increase_photo_counter.assert_has_calls([
            mock.call(),
            mock.call()
        ])
        uploader.upload.assert_has_calls([
            mock.call('mydata1', 'myphoto1.jpg'),
            mock.call('mydata2', 'myphoto2.png')
        ])

    @mock.patch('PIL.Image.open')
    def test_run_with_filters(self, image_open_mock):
        """
        Test run method with filters

        :param MagicMock image_open_mock: mock for Image.open
        """
        original_img1 = Mock()
        original_img1.format = 'JPEG'
        original_img1._getexif.return_value = 'myexifdata1'
        original_img2 = Mock()
        original_img2.format = 'PNG'
        original_img2._getexif.return_value = 'myexifdata2'
        image_open_mock.side_effect = [original_img1, original_img2]

        img1 = Mock()
        original_img1.copy.return_value = img1
        img2 = Mock()
        original_img2.copy.return_value = img2

        picker = Mock()
        picker.picked_file_paths = [
            '/myfolder/myphoto1.jpg',
            '/myfolder/myphoto2.png'
        ]

        filter1 = Mock()
        filter1_img1 = Mock()
        filter1_img2 = Mock()
        filter1.execute.side_effect = [filter1_img1, filter1_img2]
        filter2 = Mock()
        filter2_img1 = Mock()
        filter2_img2 = Mock()
        filter2.execute.side_effect = [filter2_img1, filter2_img2]

        filter2_img1.save.side_effect = self._image_save_side_effect
        filter2_img2.save.side_effect = self._image_save_side_effect

        uploader = Mock()

        photos_picker = PhotosPicker(picker, (filter1, filter2), uploader)
        photos_picker.run()

        picker.initialize.assert_called_once()
        picker.scan.assert_called_once()

        image_open_mock.assert_has_calls([
            mock.call('/myfolder/myphoto1.jpg'),
            mock.call('/myfolder/myphoto2.png')
        ])

        original_img1.copy.assert_called_once()
        original_img2.copy.assert_called_once()

        filter1.execute.assert_has_calls([
            mock.call(img1, 'myexifdata1'),
            mock.call(img2, 'myexifdata2'),
        ])

        filter2.execute.assert_has_calls([
            mock.call(filter1_img1, 'myexifdata1'),
            mock.call(filter1_img2, 'myexifdata2'),
        ])

        filter2_img1.save.assert_called_with(InstanceOf(BytesIO), 'JPEG')
        filter2_img2.save.assert_called_with(InstanceOf(BytesIO), 'PNG')

        uploader.initialize.assert_called_once()
        uploader.increase_photo_counter.assert_has_calls([
            mock.call(),
            mock.call()
        ])
        uploader.upload.assert_has_calls([
            mock.call('binarydata_JPEG', 'myphoto1.jpg'),
            mock.call('binarydata_PNG', 'myphoto2.png')
        ])

    @staticmethod
    def _image_save_side_effect(bytesio, img_format):
        """
        Method for image save mock side effect

        :param BytesIO bytesio: BytesIO instance for writing image
        :param str img_format : image format (JPEG, PNG...)
        """
        bytesio.write('binarydata_' + img_format)
