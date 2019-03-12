from typing import Dict

from BackEnd.Database import base
from BackEnd.Documents import TDocument, Document

import datetime

from frozendict import frozendict

from sqlalchemy import Column, String, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import relationship


class TDBDocument(TDocument, DeclarativeMeta):
    pass


class SADocument(Document, base, metaclass=TDBDocument):
    __tablename__ = 'document'

    file_id = Column(Integer, primary_key=True)
    path = Column(String)
    hash = Column(String)
    date_parse = Column(TIMESTAMP)
    date_create = Column(TIMESTAMP)
    date_edit = Column(TIMESTAMP)
    file_size = Column(Integer)
    num_words = Column(Integer)
    keywords = relationship("DBKeywordInstance", backref='document', cascade="all, delete-orphan")

    keyword_map = {}
    safe_keyword_map = None

    def __init__(self, *args, **kwargs):
        for keyword in self.keywords:
            self.keyword_map.update({keyword.get_word():keyword.get_count()})
        self.safe_keyword_map = frozendict(self.keyword_map)
        base.__init__(self, *args, **kwargs)

    def get_hash(self) -> str:
        return self.hash

    def get_keywords(self) -> Dict[str, int]:
        return dict(self.safe_keyword_map)

    def get_parse_date(self) -> datetime:
        return self.date_parse

    def get_create_date(self) -> datetime:
        return self.date_create

    def get_edit_date(self) -> datetime:
        return self.date_edit

    def get_file_path(self) -> str:
        return self.path

    def get_file_size(self) -> int:
        return self.file_size

    def get_num_words(self) -> int:
        return self.num_words

    def _get_db_keyword(self, word: str):
        for keyword in self.keywords:
            if keyword.get_word() == word:
                return keyword
        return None

    def add_keyword(self, word: str, count: int):
        if self.occurs(word):
            self._get_db_keyword(word).set_count(count)
        self.keyword_map[word] = count
