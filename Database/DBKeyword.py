from sqlalchemy import Column, String, Integer
from Database.DBBase import base


class DBKeyword(base):
	__tablename__ = 'keyword'

	keyword_id = Column(Integer, primary_key=True)
	keyword = Column(String)

	def get_name(self) -> str:
		return self.keyword
