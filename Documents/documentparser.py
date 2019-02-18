from abc import ABC, abstractmethod

from Documents.document import Document


class TDocumentParser(type):
    pass


class DocumentParser(ABC):
    __metaclass__ = TDocumentParser

    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """
        Returns True if this parser can parse the given file.
        :param file_path: the path of the file
        :return: True if this parser can parse the file
        """
        pass

    @abstractmethod
    def parse(self, file_path: str) -> Document:
        """
        Parses a file at the given path into a Document instance
        :param file_path: The path of the file to parse
        :return: A document instance representing the parsed file
        """
        pass
