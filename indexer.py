import dropbox
from octosearch.indexer import File
from io import TextIOWrapper


class DropboxIndexer():

    def index(self, conf):
        dbx = dropbox.Dropbox(conf['token'])

        dirstack = [conf['path']]

        while dirstack:
            path = dirstack.pop()

            for entry in dbx.files_list_folder(path):
                if isinstance(entry, dropbox.files.FolderMetadata):
                    dirstack.append(entry.path_lower)
                    continue

                yield DropboxFile()


class DropboxFile(File):

    _response = None

    def __init__(self, file_metadata, response):
        self._response = response
        self._response.raw.decode_content = True

        super(DropboxFile, self).__init__(self._metadata(file_metadata))

    def open_binary(self):
        return self._response.raw

    def open_text(self):
        return TextIOWrapper(self.open_binary())

    def _metadata(self, file_metadata):
        return {
            # 'title': bookmark.title,
            'url': 'https://www.dropbox.com/home' + file_metadata.path_lower,
            # 'extension': file_metadata.extension,
            # 'mimetype': 'text/html',
            'size': file_metadata.size,
            'modified': file_metadata.server_modified
        }
