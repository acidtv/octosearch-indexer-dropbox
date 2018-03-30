import dropbox
from octosearch.indexer import File


class DropboxIndexer():

    def index(self, conf):
        dbx = dropbox.Dropbox(conf['token'])

        folder_stack = [conf['path']]

        while folder_stack:
            folder = folder_stack.pop()

            for object_metadata in dbx.files_list_folder(folder):
                if isinstance(object_metadata, dropbox.files.FolderMetadata):
                    folder_stack.append(object_metadata.path_lower)
                    continue

                yield DropboxFile(dbx, object_metadata)


class DropboxFile(File):

    _dbx = None

    _file_metadata = None

    _file = None

    def __init__(self, dbx, file_metadata):
        super().__init__()
        self._file_metadata = file_metadata
        self._dbx = dbx
        self._set_properties(file_metadata)

    def open(self):
        return self._file().raw

    def _file(self):
        if not self._file:
            path = self._file_metadata.path_lower
            self._file, response = self._dbx.files_download(path)

            if response.code != 200:
                raise Exception('Could not download file from dropbox, invalid response code')

            # We don't want http `Content-Type: gzip` messing around here
            self._file.raw.decode_content = True

        return self._file

    def _set_properties(self, file_metadata):
        self.url = 'https://www.dropbox.com/home' + file_metadata.path_lower,
        self.size = file_metadata.size,
        self.modified = file_metadata.server_modified
