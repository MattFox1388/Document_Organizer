from abc import ABC, ABCMeta, abstractmethod

from documentparser import DocumentParser
from storagebackend import StorageBackend


class TFileCrawler(ABCMeta):
    pass


class FileCrawler(ABC):

    _parsers = {}

    def _get_backend(self):
        return self._backend

    def _get_parser(self, extension: str):
        return self._parsers.get(extension)

    def register_parser(self, parser: DocumentParser, overwrite: bool = False):
        for ext in parser.get_compatible_extensions():
            if overwrite or ext not in self._parsers:
                self._parsers[ext] = parser

    def register(self, parser: DocumentParser, ext: str):
        self._parsers[ext] = parser

    @abstractmethod
    def crawl(self, path: str):
        pass

    @abstractmethod
    def stop(self):
        pass

    def __init__(self, backend: StorageBackend):
        self._backend = backend
