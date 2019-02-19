from Documents.document import Document
from Documents.documentbackend import DocumentBackend
from typing import Collection, Mapping
from sqlalchemy import create_engine, Column, String, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


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

	def close(self):
		"""
		Frees all hardware resources that this backend uses.
		As sessions are made per method, nothing should need to be closed.
		:return: None
		"""
		return

	# TODO: Implement
	def store(self, docs: Collection[Document]) -> bool:
		"""
		Stores multiple documents into this backend that can be retrieved later.
		:param docs: A collection of documents that will be stored.
		:return: True if documents were stored successfully, False otherwise.
		"""
		pass

	# TODO: Implement
	def get(self, keyword: str) -> Collection[Document]:
		"""
		Returns any documents that contain the given keyword.
		:param keyword: The keyword in question
		:return: Collection of documents
		"""
		session = sessionmaker(self.db)

		document_query = session.query(DBDocument)\
			.filter(DBDocument.keywords.in_(keyword)).all()


		documents = []
		for document in document_query:

		return documents

	# TODO: Implement
	def get_by_path(self, path: str) -> Document:
		"""
		Returns the document associated with a specific file path.
		If there is no Document already stored for that path this will return None.
		:param path: the path of the document
		:return: Document for the path
		"""
		pass

	# TODO: Implement
	def get_duplicates(self) -> Mapping[int, Collection[Document]]:
		"""
		Returns all duplicates that are in this backend.
		The returned map has document hash codes as keys and Collection of all documents with that hash code as values.
		:return: Map of all duplicates found
		"""
		pass

	# TODO: Implement
	def get_duplicates_of(self, doc: Document) -> Collection[Document]:
		"""
		Returns all duplicates of the given document.
		It is HIGHLY recommended to override this method for each backend since default implementation gathers all
		duplicates to check.
		If there are no duplicates for the document the returned Collection will be empty.
		:param doc: Document to find duplicates of
		:return: Collection of documents
		"""
		pass


# TODO: Move these classes to their own files
base = declarative_base()





class DBKeyword(base):
	__tablename__ = 'keyword'

	keyword_id = Column(Integer, primary_key=True)
	keyword = Column(String)


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
	keywords = relationship(DBKeyword, backref='document')


class DBKeywordInstance(base):
	_tablename = 'keyword_instance'

	keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), primary_key=True)
	file_id = Column(Integer, ForeignKey("document.file_id"), primary_key=True)


