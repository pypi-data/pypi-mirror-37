from photospicker.uploader.abstract_uploader import AbstractUploader
from dropbox.dropbox import Dropbox
from dropbox.exceptions import ApiError
from dropbox.files import DeleteError


class DropboxUploader(AbstractUploader):

    def __init__(self, api_token):
        """
        Constructor

        :param str api_token: Dropbox api token
        """
        super(DropboxUploader, self).__init__()
        self._dbx = Dropbox(api_token)

    def initialize(self):
        """Clear remote directory"""
        # Clear application directory
        try:
            self._dbx.files_delete_v2('/photos')
        except ApiError as e:
            if not isinstance(e.error, DeleteError) \
                    or not e.error.is_path_lookup():
                raise e

    def upload(self, binary, original_filename):
        """
        Upload or copy files to destination

        :param str binary           : binary data to upload
        :param str original_filename: original file name
        """
        # Upload file
        path = "/photos/{photo_name}".format(
            photo_name=self._build_filename(original_filename)
        )
        self._dbx.files_upload(binary, path)
