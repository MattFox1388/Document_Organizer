from Documents.document import Document
from Documents.documentbackend import DocumentBackend
from typing import Collection, Mapping
from sqlalchemy import create_engine, Column, String, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class PostgresBackend(DocumentBackend):
	db = False

	def __new__(cls, host: str, dbname: str, user: str, password: str, port: str):
		return super(PostgresBackend, cls).__new__(cls)

	def __init__(self, host: str, dbname: str, user: str, password: str, port: str):
		# Open connection
		database = "postgresql+psycopg2://%s:%s@%s:%s/%s"%(
			user, password, host, port, dbname)
		self.db = create_engine(database)
		super(PostgresBackend, self).__init__()

	# TODO: Implement
	def store(self, docs: Collection[Document]) -> bool:
		pass

	# TODO: Implement
	def get(self, keyword: str) -> Collection[Document]:
		pass

	# TODO: Implement
	def get_duplicates(self) -> Mapping[int, Collection[Document]]:
		pass

	# TODO: Implement
	def get_duplicates_of(self, doc: Document) -> Collection[Document]:
		pass


# TODO: Move these classes to their own files
base = declarative_base()


class DBDocument(base):
	__tablename__ = 'document'

	file_id = Column(Integer, primary_key=True)
	path = Column(String)
	name = Column(String)
	ext = Column(String)
	hash = Column(Integer)
	date_parse = Column(TIMESTAMP)
	date_create = Column(TIMESTAMP)
	date_edit = Column(TIMESTAMP)


class DBKeyword(base):
	__tablename__ = 'keyword'

	keyword_id = Column(Integer, primary_key=True)
	keyword = Column(String)


class DBKeywordInstance(base):
	_tablename = 'keyword_instance'

	keyword_id = Column(Integer, primary_key=True)
	file_id = Column(Integer, primary_key=True)

