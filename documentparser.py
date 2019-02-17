from abc import ABC, abstractmethod

from document import Document


class TDocumentParser(type):
    pass


class DocumentParser(ABC):
    __metaclass = TDocumentParser

    @abstractmethod
    def parse(self, file_path: str) -> Document:
        """
        Parses a file at the given path into a Document instance
        :param file_path: The path of the file to parse
        :return: A document instance representing the parsed file
        """
        pass
