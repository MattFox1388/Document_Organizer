import datetime
from abc import ABC, ABCMeta
from typing import Mapping

import utc


class TDocument(type):
    __metaclass__ = ABCMeta
    pass


class Document(ABC):
    __metaclass = TDocument

    def get_hash(self) -> int:
        """
        Returns the hash code of this document.
        :return: Documents hash
        """
        return self._hash

    def get_keywords(self) -> Mapping[str,int]:
        """
        Returns a map of all the keywords in this document and their occurrences.
        :return: Map of keywords to occurrences
        """
        return self._keywords

    def get_occurrences(self, keyword: str) -> int:
        """
        Returns the number of times a given keyword occurs in this document.
        :param keyword: keyword in question
        :return: Occurrences of the keyword
        """
        keys = self.get_keywords()
        if keyword in keys:
            return keys[keyword]
        return 0

    def occurs(self, keyword: str):
        """
        Returns True if the given keyword exists in this document.
        :param keyword: The keyword in question
        :return: True if the keyword exists, False otherwise
        """
        return self.get_occurrences(keyword) > 0

    def get_Parse_Date(self) -> datetime:
        """
        Returns the time when this document was parsed last.
        :return: Last parse time
        """
        return self._parse_date

    def get_file_path(self) -> str:
        """
        Returns the path of the file for this document.
        :return: path of this document
        """
        return self._file_path

    def is_same(self, doc) -> bool:
        """
        Returns True whether the given document is a duplicate of this one.
        :param doc: other document to compare
        :return: True if they have the same hash code, False otherwise
        """
        return self.get_hash() == doc.get_hash()

    def __eq__(self, other):
        if isinstance(other, Document):
            return self.get_hash() == other.get_hash() \
                and self.get_keywords() == other.get_keywords() \
                and self.get_Parse_Date() == other.get_Parse_Date() \
                and self.get_file_path() == other.get_file_path()
        return False

    def __init__(self, hash_val: int, keywords: Mapping[str,int], file_path: str, parse_date: datetime = utc.now()):
        self._hash = hash_val
        self._keywords = keywords
        self._file_path = file_path
        self._parse_date = parse_date

