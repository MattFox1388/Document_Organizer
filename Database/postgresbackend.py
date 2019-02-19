from .DBKeywordInstance import DBKeywordInstance
from .DBKeyword import DBKeyword
from .DBDocument import DBDocument
from Documents.document import Document
from Documents.documentbackend import DocumentBackend
from typing import Collection, Mapping
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgresBackend(DocumentBackend):
	db = False
	session = False

	def __new__(cls, host: str, dbname: str, user: str, password: str, port: str):
		return super(PostgresBackend, cls).__new__(cls)

	def __init__(self, host: str, dbname: str, user: str, password: str, port: str):
		# Open connection
		database = "postgresql+psycopg2://%s:%s@%s:%s/%s"%(
			user, password, host, port, dbname)
		self.db = create_engine(database)
		self.session = sessionmaker(self.db)
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
		session = self.session()
		try:
			for doc in docs:
				newdoc = DBDocument(path=doc.get_file_path())
				for keyword in doc.get_keywords():
					kw = session.query(DBKeyword).filter(DBKeyword.keyword == keyword[0]).all()
					if len(kw) == 0:
						kw = DBKeyword(keyword[0])
						session.add(kw)
					else:
						kw = kw[0]
					session.add(DBKeywordInstance(file_id=newdoc,
												keyword_id=kw,
												count=keyword[1]))
				session.add()
		except:
			session.rollback()
			return False
		session.commit()
		return True

	def get(self, keyword: str) -> Collection[Document]:
		"""
		Returns any documents that contain the given keyword.
		:param keyword: The keyword in question
		:return: Collection of documents
		"""
		session = self.session()

		documents = session.query(DBDocument)\
			.filter(DBDocument.instance.keyword.in_(keyword)).all()
		return documents

	def get_by_path(self, path: str) -> Document:
		"""
		Returns the document associated with a specific file path.
		If there is no Document already stored for that path this will return None.
		:param path: the path of the document
		:return: Document for the path
		"""
		session = self.session()

		documents = session.query(DBDocument)\
			.filter(DBDocument.path == path).all()
		return documents
		pass

	# TODO: Implement
	def get_duplicates(self) -> Mapping[int, Collection[Document]]:
		"""
		Returns all duplicates that are in this backend.
		The returned map has document hash codes as keys and Collection of all documents with that hash code as values.
		:return: Map of all duplicates found
		"""
		pass

	def get_duplicates_of(self, doc: Document) -> Collection[Document]:
		"""
		Returns all duplicates of the given document.
		It is HIGHLY recommended to override this method for each backend since default implementation gathers all
		duplicates to check.
		If there are no duplicates for the document the returned Collection will be empty.
		:param doc: Document to find duplicates of
		:return: Collection of documents
		"""
		session = self.session()

		documents = session.query(DBDocument)\
			.filter(DBDocument.hash == doc.get_hash())\
			.filter(DBDocument.path != doc.get_file_path())
		return documents
