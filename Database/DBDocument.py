import datetime
from collections import Mapping

import frozendict as frozendict

from Database import DBKeywordInstance
from Documents.document import Document
from sqlalchemy import Column, String, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class DBDocument(base, Document):
	__tablename__ = 'document'

	file_id = Column(Integer, primary_key=True)
	path = Column(String)
	name = Column(String)
	ext = Column(String)
	hash = Column(Integer)
	date_parse = Column(TIMESTAMP)
	date_create = Column(TIMESTAMP)
	date_edit = Column(TIMESTAMP)
	keywords = relationship(DBKeywordInstance, backref='document')

	keyword_map = {}
	safe_keyword_map = None

	def __init__(self):
		for keyword in self.keywords:
			self.keyword_map[keyword.get_word()]
		self.safe_keyword_map = frozendict(self.keyword_map)

	def get_hash(self) -> int:
		return self.hash

	def get_keywords(self) -> Mapping[str, int]:
		return self.safe_keyword_map

	def get_parse_date(self) -> datetime:
		return self.date_parse

	def get_file_path(self) -> str:
		return self.path

	def _get_db_keyword(self, word: str) -> DBKeywordInstance:
		for keyword in self.keywords:
			if keyword.get_word() == word:
				return keyword
		return None

	def add_keyword(self, word: str, count: int):
		if self.occurs(word):
			self._get_db_keyword(word).set_count(count)
		self.keyword_map[word] = count