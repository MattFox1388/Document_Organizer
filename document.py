import datetime
from abc import ABC
from typing import Mapping


class TDocument(type):
    pass


class Document(ABC, TDocument):

    def get_hash(self) -> int:
        return self._hash

    def get_keywords(self) -> Mapping[str,int]:
        return self._keywords

    def get_Parse_Date(self) -> datetime:
        return self._parse_date

    def get_file_path(self) -> str:
        return self._file_path

    def is_same(self, doc: TDocument) -> bool:
        return self.get_hash() == doc.get_hash()

    def __init__(self, hash: int, keywords: Mapping[str,int],parse_date: datetime, file_path: str):
        self._hash = hash
        self._keywords = keywords
        self._parse_date = parse_date
        self._file_path = file_path