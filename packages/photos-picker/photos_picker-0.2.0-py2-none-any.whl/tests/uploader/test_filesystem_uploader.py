from unittest import TestCase
from photospicker.uploader.filesystem_uploader import FilesystemUploader
from mock import MagicMock
from photospicker.exception.picker_exception import PickerException
import mock


class TestFilesystemUploader(TestCase):
    """Test class for FilesystemUploader"""

    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_initialize_directory_not_found(self, is_dir_mock, listdir_mock):
        """
        Test that an exception is launched if the directory is not found

        :param MagicMock is_dir_mock: is_dir function mock
        :param MagicMock listdir_mock: listdir function mock
        """
        is_dir_mock.return_value = False

        with self.assertRaises(PickerException) as cm:
            sut = FilesystemUploader('/root/myfolder')
            sut.initialize()

        is_dir_mock.assert_called_with('/root/myfolder')

        self.assertEqual(
            "Directory /root/myfolder not found",
            cm.exception.message
        )

    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_initialize_directory_not_empty(self, is_dir_mock, listdir_mock):
        """
        Test that an exception is launched if the directory is not empty

        :param MagicMock is_dir_mock: is_dir function mock
        :param MagicMock listdir_mock: listdir function mock
        """
        is_dir_mock.return_value = True
        listdir_mock.return_value = ['myfile']

        with self.assertRaises(PickerException) as cm:
            sut = FilesystemUploader('/root/myfolder')
            sut.initialize()

        is_dir_mock.assert_called_with('/root/myfolder')
        listdir_mock.assert_called_with('/root/myfolder')

        self.assertEqual(
            "Directory /root/myfolder not empty",
            cm.exception.message
        )

    @mock.patch('__builtin__.open')
    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_upload(self, is_dir_mock, listdir_mock, mock_open):
        """
        Test upload (copy)

        :param MagicMock is_dir_mock: is_dir function mock
        :param MagicMock listdir_mock: listdir function mock
        :param MagicMock mock_open: open built'in function mock
        """
        is_dir_mock.return_value = True
        listdir_mock.return_value = []

        handle = MagicMock()

        mock_open.return_value = handle

        sut = FilesystemUploader('/root/myfolder')
        sut.initialize()
        sut.upload('mydata', 'myphoto.jpg')

        mock_open.assert_called_once_with('/root/myfolder/photo0.jpg', 'w')
        handle.__enter__().write.assert_called_once_with('mydata')
