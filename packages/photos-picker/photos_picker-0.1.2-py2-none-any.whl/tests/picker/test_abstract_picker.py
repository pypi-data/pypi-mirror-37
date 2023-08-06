from photospicker.picker.abstract_picker import AbstractPicker
from unittest import TestCase
from mock import MagicMock  # noqa
import unittest_dataprovider
import mock


class DummyPicker(AbstractPicker):
    """Dummy class for testing AbstractPicker"""

    def scan(self):
        """Dummy abstract method"""
        pass

    @property
    def files_to_scan(self):
        """
        Getter for _files_to_scan

        :return: list
        """
        return self._files_to_scan


class TestAbstractPicker(TestCase):
    """Unit tests for AbstractPicker"""

    def test_wrong_patterns_format(self):
        """Test that an exception is launched """
        with self.assertRaises(TypeError) as cm:
            DummyPicker('', 20, patterns='test')

        self.assertEqual(
            "patterns argument must be a list",
            cm.exception.message
        )

    @staticmethod
    def provider_analyse():
        """Data provider for test_initialize"""
        return (
            (None, ['myphoto1.jpg', 'myphoto2.JPEG', 'myphoto3.png']),
            (['*.jpg', '*.jpeg'], ['myphoto1.jpg', 'myphoto2.JPEG']),
        )

    @unittest_dataprovider.data_provider(provider_analyse)
    @mock.patch('os.walk')
    def test_initialize(self, patterns, expected_files_to_scan, walk_mock):
        """
        Test initialize method

        :param list|None patterns              : patterns passed
                                                 to the constructor
        :param list      expected_files_to_scan: list that should be in
                                                 the _files_to_scan property
        :param MagicMock walk_mock             : mock for walk function
        """

        walk_mock.return_value = [['', [], [
            'myphoto1.jpg',
            'myphoto2.JPEG',
            'myphoto3.png'
        ]]]

        sut = DummyPicker('mypath', 20, patterns=patterns)
        sut.initialize()

        walk_mock.assert_called_with('mypath')
        self.assertEqual(expected_files_to_scan, sut.files_to_scan)
