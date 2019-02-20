import os
from abc import ABC, abstractmethod
from collections import Collection

from Documents.document import Document


class TDocumentParser(type):
    pass


class DocumentParser(ABC):
    __metaclass__ = TDocumentParser

    @abstractmethod
    def get_compatible_extensions(self) -> Collection[str]:
        """
        Returns a collection of all file extensions that this parser can parse into documents.
        :return: collection of file extensions
        """
        pass

    def can_parse(self, file_path: str) -> bool:
        """
        Returns True if this parser can parse the given file.
        :param file_path: the path of the file
        :return: True if this parser can parse the file
        """
        return os.path.splitext(file_path) in self.get_compatible_extensions()

    @abstractmethod
    def parse(self, file_path: str) -> Document:
        """
        Parses a file at the given path into a Document instance
        :param file_path: The path of the file to parse
        :return: A document instance representing the parsed file
        """
        pass

    def compute_hash(self, file_path: str) -> int:
        f = open(file_path, 'r')
        hash = 31