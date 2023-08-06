from photospicker.picker.abstract_picker import AbstractPicker
from PIL import Image
from PIL import ExifTags
import operator


class LastPhotosPicker(AbstractPicker):
    """Pick the lastest photos by DateTimeOriginal in EXIF data"""

    def scan(self):
        """Scan the given path for building picked file paths list"""
        data_to_sort = {}

        scanned = 0
        self._notify_progress(scanned)
        for filepath in self._files_to_scan:
            img = Image.open(filepath)
            exif_data = img._getexif()

            if exif_data is None:
                continue

            for key in exif_data.keys():
                if ExifTags.TAGS.get(key) != 'DateTimeOriginal':
                    continue

                data_to_sort[filepath] = exif_data[key]

            scanned += 1
            self._notify_progress(scanned)

        self._notify_end()

        sorted_filenames = sorted(
            data_to_sort.items(),
            key=operator.itemgetter(1),
            reverse=True
        )

        for key, data in enumerate(sorted_filenames):
            if key >= self._photos_count:
                break
            self._picked_file_paths.append(data[0])
