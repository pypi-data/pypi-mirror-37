from photospicker.picker.abstract_picker import AbstractPicker
import random


class RandomPicker(AbstractPicker):
    """Pick photos randomly"""

    def scan(self):
        """Scan the given path for building picked file paths list"""
        self._notify_progress(0)
        random.shuffle(self._files_to_scan)
        self._notify_progress(len(self._files_to_scan))
        self._notify_end()

        self._picked_file_paths = self._files_to_scan[0:self._photos_count]
