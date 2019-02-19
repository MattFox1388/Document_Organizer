from Documents.document import Document
from .DBKeyword import DBKeyword
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
	instance = relationship(DBKeyword, backref='instance')


def get_hash(self):
	return self.hash


def get_keywords(self):
	keywords = []
	for i in self.instance:
		keywords.append((i.keyword.keyword, i.count))
	return


def get_parse_date(self):
	return self.date_parse


def get_file_path(self):
	return self.path
