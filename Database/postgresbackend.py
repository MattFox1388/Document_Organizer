from Documents.document import Document
from Documents.documentbackend import DocumentBackend
import psycopg2 # PostgreSQL database adapter -  pip install psycopg2
from typing import Collection, Mapping


class PostgresBackend(DocumentBackend):
	# psycopg2 database session
	conn = False
	# psycopg2 cursor - Used for making SQL queries
	cr = False

	def __new__(mcs, host: str, dbname: str, user: str, password: str, port: str):
		return super(PostgresBackend, mcs).__new__(mcs)

	def __init__(cls, host: str, dbname: str, user: str, password: str, port: str):
		# Open connection
		cls.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
		cls.cr = cls.conn.cursor()

		super(PostgresBackend, cls).__init__()

	def __del__(self):
		# Close connection
		self.cr.close()
		self.conn.close()

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
