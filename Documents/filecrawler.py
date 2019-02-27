from abc import ABC, ABCMeta, abstractmethod

from Documents.documentbackend import DocumentBackend
from Documents.documentparser import DocumentParser


class TFileCrawler(ABCMeta):
    pass


class FileCrawler(ABC, metaclass=TFileCrawler):

    _parsers = {}

    def _get_backend(self):
        return self._backend

    def _get_parser(self, extension: str):
        return self._parsers.get(extension)

    def register_parser(self, parser: DocumentParser, overwrite: bool = False):
        for ext in parser.get_compatible_extensions():
            if overwrite or ext not in self._parsers:
                self._parsers[ext] = parser

    @abstractmethod
    def crawl(self, path: str):
        pass

    def __init__(self, backend: DocumentBackend):
        self._backend = backend
