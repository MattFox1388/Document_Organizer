from abc import ABC, abstractmethod

from document import TDocument


class TParser(type):
    pass


class Parser(ABC, TParser):

    @abstractmethod
    def parse(self, file_path: str) -> TDocument:
        """
        Parses a file at the given path into a Document instance
        :param file_path: The path of the file to parse
        :return: A document instance representing the parsed file
        """
        pass
