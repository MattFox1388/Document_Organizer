from .DBKeyword import DBKeyword
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class DBKeywordInstance(base):
	_tablename = 'keyword_instance'

	keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), primary_key=True)
	file_id = Column(Integer, ForeignKey("document.file_id"), primary_key=True)
	count = Column(Integer)
	keyword = relationship(DBKeyword)

