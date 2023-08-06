from unittest import TestCase
from photospicker.picker.random_picker import RandomPicker
from mock import MagicMock  # noqa
import mock


class TestRandomPicker(TestCase):
    """Test class for RandomPicker"""

    @mock.patch('random.shuffle')
    @mock.patch('os.walk')
    def test_scan(self, walk_mock, shuffle_mock):
        """
        Test random pick

        :param MagicMock walk_mock   : mock for os.walk
        :param MagicMock shuffle_mock: mock for random.shuffle
        """
        walk_mock.return_value = [['', [], [
            'myphoto1.jpg',
            'myphoto2.jpg',
            'myphoto3.jpg',
            'myphoto4.jpg'
        ]]]

        shuffle_mock.side_effect = self._shuffle_mock_side_effect

        sut = RandomPicker('', 2)
        sut.initialize()
        sut.scan()

        shuffle_mock.assert_called_once()

        self.assertEqual(
            ['myphoto3.jpg', 'myphoto2.jpg'],
            sut.picked_file_paths
        )

    def _shuffle_mock_side_effect(self, files):
        """
        Side effect for shuffle mock

        :param list files: file list
        """

        self.assertEqual(files, [
            'myphoto1.jpg',
            'myphoto2.jpg',
            'myphoto3.jpg',
            'myphoto4.jpg'
        ])

        del files[:]
        files.append('myphoto3.jpg')
        files.append('myphoto2.jpg')
        files.append('myphoto4.jpg')
        files.append('myphoto1.jpg')
