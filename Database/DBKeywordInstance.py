from Database.DBBase import base
from Database import DBDocument
from Database.DBKeyword import DBKeyword
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class DBKeywordInstance(base):
	__tablename__ = 'keyword_instance'

	keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), primary_key=True)
	keyword = relationship(DBKeyword)
	file_id = Column(Integer, ForeignKey("document.file_id"), primary_key=True)
	count = Column(Integer)

	def get_document(self):
		return self.document

	def get_word(self) -> str:
		return self.keyword.get_name()

	def get_count(self) -> int:
		return self.count

	def set_count(self, new_count: int):
		count = new_count
