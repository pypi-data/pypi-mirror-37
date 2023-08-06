class EndUploadEvent(object):
    """Event dispatched when an upload starts"""

    def __init__(self, filepath, uploaded_files, files_to_upload):
        """
        Constructor

        :param str filepath       : file uploaded
        :param int uploaded_files : total files uploaded count
        :param int files_to_upload: total files to upload count
        """
        self._filepath = filepath
        self._uploaded_files = uploaded_files
        self._files_to_upload = files_to_upload

    @property
    def filepath(self):  # pragma: no cover
        """
        Getter for the file uploaded

        :return str
        """
        return self._filepath

    @property
    def uploaded_files(self):  # pragma: no cover
        """
        Getter for the total files uploaded count

        :return int
        """
        return self._uploaded_files

    @property
    def files_to_upload(self):  # pragma: no cover
        """
        Getter for the total files to upload count

        :return int
        """
        return self._files_to_upload
