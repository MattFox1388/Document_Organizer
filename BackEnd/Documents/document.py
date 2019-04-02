import os
import datetime
from abc import ABC, abstractmethod

import utc


class Document(ABC):

    def get_term_frequency(self, term: str) -> float:
        return self.get_occurrences(term) / self.get_total_words()

    @abstractmethod
    def get_hash(self) -> str:
        """
        Returns the hash code of this document.
        :return: Documents hash
        """
        pass

    @abstractmethod
    def get_keywords(self):
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

    @abstractmethod
    def get_file_size(self) -> int:
        """
        Returns the size of the file for this document.
        :return: size of this document
        """
        pass

    @abstractmethod
    def get_num_words(self) -> int:
        """
        Returns the number of words in the document.
        :return: number of words in document
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
                and self.get_edit_date() == other.get_edit_date() \
                and self.get_file_size() == other.get_file_size() \
                and self.get_num_words() == other.get_num_words()
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

    def get_file_size(self):
        return self._file_size

    def get_num_words(self):
        return self._num_words

    '''This method uses ctime to find creation time (Windows), or last metadata change (Unix). 
       Second datetime in tuple will be the last modified datetime'''

    @staticmethod
    def find_create_and_mod(file_path) -> (datetime, datetime):
        # check whether windows, linux or mac
        stat = os.stat(file_path)
        create_date = datetime.datetime.fromtimestamp(stat.st_ctime)
        mod_date = datetime.datetime.fromtimestamp(stat.st_mtime)
        return create_date, mod_date

    def __init__(self, hash_val: str, keywords, file_path: str, create_date: datetime, edit_date: datetime, file_size:int, num_words:int, parse_date: datetime = utc.now()):
        self._hash = hash_val
        self._keywords = keywords
        self._file_path = file_path
        self._parse_date = parse_date
        self._create_date = create_date
        self._edit_date = edit_date
        self._file_size = file_size
        self._num_words = num_words

    def __str__(self):
        return self.get_file_path()

    def __repr__(self):
        return str(self)