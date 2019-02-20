from Database import DBDocument
from .DBKeyword import DBKeyword
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class DBKeywordInstance(base):
	__tablename__ = 'keyword_instance'

	keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), primary_key=True)
	file_id = Column(Integer, ForeignKey("document.file_id"), primary_key=True)
	count = Column(Integer)
	keyword = relationship(DBKeyword)

	def get_document(self) -> DBDocument:
		return self.document

	def get_word(self) -> str:
		return self.keyword.get_name()

	def get_count(self) -> int:
		return self.count

	def set_count(self, new_count: int):
		count = new_count