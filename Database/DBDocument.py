import datetime
from collections import Mapping

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

	def __init__(self):
		for keyword in self.keywords:
			self.keyword_map[keyword.get_word()]

	def get_hash(self) -> int:
		return self.hash

	def get_keywords(self) -> Mapping[str, int]:
		return self.keyword_map

	def get_occurrences(self, keyword: str) -> int:
		if keyword in self.get_keywords():
			return self.get_keywords()[keyword]
		return 0

	def occurs(self, keyword: str):
		return self.get_occurrences(keyword) > 0

	def get_parse_date(self) -> datetime:
		return self.date_parse

	def get_file_path(self) -> str:
		return self.path