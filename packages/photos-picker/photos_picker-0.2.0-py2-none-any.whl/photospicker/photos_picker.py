from event.start_upload_event import StartUploadEvent
from event.end_upload_event import EndUploadEvent
from event.start_filter_event import StartFilterEvent
from event.end_filter_event import EndFilterEvent
from zope.event import notify
from PIL import Image
from io import BytesIO
from photospicker.picker.abstract_picker import AbstractPicker  # noqa
from photospicker.uploader.abstract_uploader import AbstractUploader  # noqa
import ntpath


class PhotosPicker:
    """
    Select photos accorting to a chosen strategy and
    copy them to a chosen destination
    """

    def __init__(self, picker, filters, uploader):
        """
        Constructor

        :param AbstractPicker picker    : photo selection strategy
        :param tuple filters            : filters
        :param AbstractUploader uploader: upload strategy
        """
        self._picker = picker
        self._filters = filters
        self._uploader = uploader

    def run(self):
        """Run photo selection and upload"""
        self._picker.initialize()
        self._picker.scan()

        total_picked = len(self._picker.picked_file_paths)

        self._uploader.initialize()
        for key, filepath in enumerate(self._picker.picked_file_paths):
            rank = key + 1

            # If no filter is applyed, save without quality loss
            if len(self._filters) == 0:
                with open(filepath, mode='rb') as f:
                    file_content = f.read()
            else:
                original_img = Image.open(filepath)
                exif_data = original_img._getexif()
                img = original_img.copy()

                for photo_filter in self._filters:
                    notify(StartFilterEvent(photo_filter, filepath))
                    img = photo_filter.execute(img, exif_data)
                    notify(EndFilterEvent(photo_filter, filepath))

                b = BytesIO()
                img.save(b, original_img.format)
                file_content = b.getvalue()

            notify(StartUploadEvent(filepath, rank, total_picked))
            self._uploader.increase_photo_counter()
            self._uploader.upload(file_content, ntpath.basename(filepath))
            notify(EndUploadEvent(filepath, rank, total_picked))
