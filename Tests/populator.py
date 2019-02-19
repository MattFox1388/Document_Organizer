import datetime
import glob
import os

from Documents.document import Document
from Documents.documentbackend import DocumentBackend
from Documents.documentparser import DocumentParser


def populate(parser: DocumentParser, backend: DocumentBackend, root: str):
    """
    Iterates through all files and directories/subdirectories of given path and
    stores/updates the documents in the backend.
    :param parser: The Document parser to be used
    :param backend: The backend that all documents will be stored in
    :param root: the directory to iterate through
    :return: Void
    """
    for file in glob.glob(root + '*'):
        print(file)
        if os.path.isdir(file):
            populate(parser, backend, file + '\\*')
        else:
            if not parser.can_parse(file):
                continue
            mod_time = datetime.fromtimestamp(os.path.getmtime(file))
            stored_doc = backend.get_by_path(file)
            if need_to_parse(doc, mod_time, stored_doc):
                doc = parser.parse(file)
                backend.store([doc])


def need_to_parse(doc: Document, mod_time: datetime, stored: Document) -> bool:
    return stored is None or mod_time > stored.get_parse_date()


populate(None, None, '')