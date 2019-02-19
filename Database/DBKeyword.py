from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
base = declarative_base()


class DBKeyword(base):
	__tablename__ = 'keyword'

	keyword_id = Column(Integer, primary_key=True)
	keyword = Column(String)
