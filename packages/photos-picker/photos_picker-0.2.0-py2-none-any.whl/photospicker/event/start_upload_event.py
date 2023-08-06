class StartUploadEvent(object):
    """Event dispatched when an upload starts"""

    def __init__(self, filepath, upload_file_rank, files_to_upload):
        """
        Constructor

        :param str filepath        : file which starts to be uploaded
        :param int upload_file_rank: rank of the file in upload queue
        :param int files_to_upload : total files to upload count
        """
        self._filepath = filepath
        self._upload_file_rank = upload_file_rank
        self._files_to_upload = files_to_upload

    @property
    def filepath(self):  # pragma: no cover
        """
        Getter for the file which starts to be uploaded

        :return str
        """
        return self._filepath

    @property
    def upload_file_rank(self):  # pragma: no cover
        """
        Getter for the rank of the file in upload queue

        :return int
        """
        return self._upload_file_rank

    @property
    def files_to_upload(self):  # pragma: no cover
        """
        Getter for the total files to upload count

        :return int
        """
        return self._files_to_upload
