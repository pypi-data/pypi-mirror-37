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

    @staticmethod
    def provider_initialize_multiple_and_excluded_paths():
        """Data provider for test_initialize_multiple_and_excluded_paths"""
        return (
            ([], [
                '/mypath1/folder1/myphoto1.jpg',
                '/mypath1/folder1/myphoto2.JPEG',
                '/mypath2/myphoto3.png',
                '/mypath2/folder1/myphoto4.png'
            ]),
            (['/mypath1'], [
                '/mypath2/myphoto3.png',
                '/mypath2/folder1/myphoto4.png'
            ]),
            (['/mypath2'], [
                '/mypath1/folder1/myphoto1.jpg',
                '/mypath1/folder1/myphoto2.JPEG',
            ]),
            (['/mypath2/folder1'], [
                '/mypath1/folder1/myphoto1.jpg',
                '/mypath1/folder1/myphoto2.JPEG',
                '/mypath2/myphoto3.png'
            ])
        )

    @unittest_dataprovider.data_provider(
        provider_initialize_multiple_and_excluded_paths
    )
    @mock.patch('os.walk')
    def test_initialize_multiple_and_excluded_paths(
            self,
            excluded_paths,
            expected_files_to_scan,
            walk_mock
    ):
        """
        Test initialize method with multiple and excluded paths

        :param list excluded_paths        : excluded paths
        :param list expected_files_to_scan: expected files to scan
        :param MagicMock walk_mock        : mock for walk function
        """
        walk_mock.side_effect = [
            [
                ['/mypath1', [], []],
                ['/mypath1/folder1', [], ['myphoto1.jpg', 'myphoto2.JPEG']]
            ],
            [
                ['/mypath2', [], ['myphoto3.png']],
                ['/mypath2/folder1', [], ['myphoto4.png']]
            ]
        ]

        sut = DummyPicker(['/mypath1', '/mypath2'], 20, None, excluded_paths)
        sut.initialize()

        walk_mock.assert_has_calls([
            mock.call('/mypath1'),
            mock.call('/mypath2')
        ])

        self.assertEqual(expected_files_to_scan, sut.files_to_scan)
