from unittest import TestCase
from mock import Mock
from mock import MagicMock  # noqa
from photospicker.filter.rotate_filter import RotateFilter
import mock
import unittest_dataprovider


class TestRotateFilter(TestCase):
    """Unit tests for ResizeFilter"""

    @mock.patch('photospicker.filter.rotate_filter.ExifTags')
    def test_execute_orientationtagnotexists_shouldreturnoriginalimg(
            self,
            exif_tags_mock
    ):
        """
        Test that execute return original image
        if Orientation tag doesn't exist (normally not possible)

        :param MagicMock exif_tags_mock: mock for ExifTags
        """
        exif_tags_mock.TAGS = {123: 'mytagvalue'}

        sut = RotateFilter()
        self.assertEqual('myoriginaldata', sut.execute('myoriginaldata', {}))

    @staticmethod
    def provider_execute_noexiforientationissupplied_shouldreturnoriginalimg():
        """
        Data provider for
        test_execute_noexiforientationissupplied_shouldreturnoriginalimg

        :return: tuple
        """
        return (
            (None,),
            ({},),
            ({123: 'myexifdata'},),
            ({456: 5},)
        )

    @unittest_dataprovider.data_provider(
        provider_execute_noexiforientationissupplied_shouldreturnoriginalimg
    )
    @mock.patch('photospicker.filter.rotate_filter.ExifTags')
    def test_execute_noexiforientationissupplied_shouldreturnoriginalimg(
            self,
            exif_data,
            exif_tags_mock
    ):
        """
        Test that execute return original image
        if no exif orientation is not supplied

        :param mixed exif_data         : exif data of the original image
        :param MagicMock exif_tags_mock: mock for ExifTags
        """
        exif_tags_mock.TAGS = {123: 'mytagvalue', 456: 'Orientation'}

        sut = RotateFilter()
        self.assertEqual(
            'myoriginaldata',
            sut.execute('myoriginaldata', exif_data)
        )

    @staticmethod
    def provider_execute():
        """
        Data provider for test_execute

        :return: tuple
        """
        return (
            (False, {456: 3}, 180, False),
            (True, {456: 6}, 270, True),
            (None, {456: 8}, 90, True),
        )

    @unittest_dataprovider.data_provider(provider_execute)
    @mock.patch('photospicker.filter.rotate_filter.ExifTags')
    def test_execute(
            self,
            expand,
            exif_data,
            expected_angle,
            expected_expand,
            exif_tags_mock
    ):
        """
        Test that right params are used when applying rotation

        :param mixed expand            : expand value passed to
            filter constructor
        :param dict exif_data          : exif data of the original image
        :param int expected_angle      : expected angle to be applyed
            to original image
        :param bool expected_expand    : expected expand value to be applyed
            to original image
        :param MagicMock exif_tags_mock: mock for ExifTags
        """
        exif_tags_mock.TAGS = {456: 'Orientation'}

        original_img = Mock()

        if expand is None:
            sut = RotateFilter()
        else:
            sut = RotateFilter(expand)

        sut.execute(original_img, exif_data)

        original_img.rotate.assert_called_once_with(
            expected_angle,
            expand=expected_expand
        )
