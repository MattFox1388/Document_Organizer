import datetime
from abc import ABC, ABCMeta, abstractmethod
from typing import Mapping

import utc


class TDocument(ABCMeta):
    pass


class Document(ABC, metaclass=TDocument):
    @abstractmethod
    def get_hash(self) -> str:
        """
        Returns the hash code of this document.
        :return: Documents hash
        """
        pass

    @abstractmethod
    def get_keywords(self) -> Mapping[str,int]:
        """
        Returns a map of all the keywords in this document and their occurrences.
        :return: Map of keywords to occurrences
        """
        pass

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

    @abstractmethod
    def get_parse_date(self) -> datetime:
        """
        Returns the time when this document was parsed last.
        :return: Last parse time
        """
        pass

    @abstractmethod
    def get_create_date(self) -> datetime:
        """
        Returns the time when this document was created.
        :return: Last parse time
        """
        pass

    @abstractmethod
    def get_edit_date(self) -> datetime:
        """
        Returns the time when this document was edited last.
        :return: Last parse time
        """
        pass

    @abstractmethod
    def get_file_path(self) -> str:
        """
        Returns the path of the file for this document.
        :return: path of this document
        """
        pass

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
                and self.get_parse_date() == other.get_parse_date() \
                and self.get_file_path() == other.get_file_path() \
                and self.get_create_date() == other.get_create_date() \
                and self.get_edit_date() == other.get_edit_date()
        return False


class SimpleDocument(Document):

    def get_hash(self):
        return self._hash

    def get_keywords(self):
        return self._keywords

    def get_parse_date(self):
        return self._parse_date

    def get_create_date(self):
        return self._create_date

    def get_edit_date(self):
        return self._edit_date

    def get_file_path(self):
        return self._file_path

    def __init__(self, hash_val: str, keywords: Mapping[str,int], file_path: str, create_date: datetime, edit_date: datetime, parse_date: datetime = utc.now()):
        self._hash = hash_val
        self._keywords = keywords
        self._file_path = file_path
        self._parse_date = parse_date
        self._create_date = create_date
        self._edit_date = edit_date

    def __repr__(self):
        print('The hash value is: ' + self._hash)
        print('The file path is: ' + self._file_path)
        print('the parse date is:' + self._parse_date)
        for key, value in self._keywords.items():
            print('The word ' + key + ' has ' + value + ' occurrences.')
