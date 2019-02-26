from Database.SABase import base
from Database import SADocument
from Database.SAKeyword import SAKeyword
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class SAKeywordInstance(base):
	__tablename__ = 'keyword_instance'

	keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), primary_key=True)
	keyword = relationship(SAKeyword)
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
