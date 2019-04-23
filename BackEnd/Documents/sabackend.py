import datetime
from abc import ABCMeta
import traceback

from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from document import Document
from storagebackend import StorageBackend
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import sessionmaker, relationship

base = declarative_base()


class SAKeyword(base):
    __tablename__ = 'keyword'

    keyword_id = Column(Integer, primary_key=True, nullable=False)
    keyword = Column(String, nullable=False)

    def get_name(self) -> str:
        return self.keyword


class SAKeywordInstance(base):
    __tablename__ = 'keyword_instance'

    keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), primary_key=True, nullable=False)
    keyword = relationship(SAKeyword, lazy='joined')
    file_id = Column(Integer, ForeignKey("document.file_id"), primary_key=True)
    count = Column(Integer)
    tag = Column(Boolean, nullable=False)

    def get_document(self):
        return self.document

    def get_word(self) -> str:
        return self.keyword.get_name()

    def get_count(self) -> int:
        return self.count

    def set_count(self, new_count: int):
        count = new_count


class ABCBaseMeta(ABCMeta, DeclarativeMeta):
    pass


class SADocument(Document, base, metaclass=ABCBaseMeta):
    __tablename__ = 'document'

    file_id = Column(Integer, primary_key=True, nullable=False)
    path = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    date_parse = Column(TIMESTAMP, nullable=False)
    date_create = Column(TIMESTAMP, nullable=False)
    date_edit = Column(TIMESTAMP, nullable=False)
    file_size = Column(Integer, nullable=False)
    num_words = Column(Integer, nullable=False)
    keywords = relationship("SAKeywordInstance", backref='document', cascade="all, delete-orphan", lazy='select')

    keyword_map = {}
    safe_keyword_map = None

    def __init__(self, *args, **kwargs):
        base.__init__(self, *args, **kwargs)

    def get_hash(self) -> str:
        return self.hash

    def get_keywords(self):
        if not self.safe_keyword_map:
            self.__init__()
        return dict(self.safe_keyword_map)

    def get_occurrences(self, keyword: str) -> int:
        r = self.keyword_map.get(keyword)
        if not r:
            return r
        for k in self.keywords:
            if k.keyword.keyword == keyword:
                return k.count
        return 0

    def get_parse_date(self) -> datetime:
        return self.date_parse

    def get_create_date(self) -> datetime:
        return self.date_create

    def get_edit_date(self) -> datetime:
        return self.date_edit

    def get_file_path(self) -> str:
        return self.path

    def get_file_size(self) -> int:
        return self.file_size

    def get_num_words(self) -> int:
        return self.num_words

    def _get_db_keyword(self, word: str):
        for keyword in self.keywords:
            if keyword.get_word() == word:
                return keyword
        return None

    def add_keyword(self, word: str, count: int):
        self.keyword_map[word] = count


class SABackend(StorageBackend):
    db = None
    session = None

    def __new__(cls, host: str, dbname: str, user: str, password: str, port: str, pool_size: int = 10):
        return super(SABackend, cls).__new__(cls)

    def __init__(self, host: str, dbname: str, user: str, password: str, port: str, pool_size: int = 10):
        # Open connection
        database = "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
            user, password, host, port, dbname)
        self.db = create_engine(database, pool_size=pool_size)
        self.session = sessionmaker(self.db)

    def close(self):
        """
        Frees all hardware resources that this backend uses.
        As sessions are made per method, nothing should need to be closed.
        :return: None
        """
        return

    def get_total_document_count(self) -> int:
        return self.session().query(SADocument).count()

    def store(self, docs) -> bool:
        """
        Stores multiple documents into this backend that can be retrieved later.
        :param docs: A collection of documents that will be stored.
        :return: True if documents were stored successfully, False otherwise.
        """
        session = self.session()
        try:
            for document in docs:
                # Check if all keywords are already in database.  If not, add them.
                for keyword, count in document.get_keywords().items():
                    kw = SAKeyword(keyword=keyword)
                    instance = session.query(SAKeyword).filter(SAKeyword.keyword == keyword).first()
                    if instance:
                        kw = instance
                    else:
                        session.add(kw)

                # Check to see if the document exists and if the hash matches
                doc_instance = session.query(SADocument).filter(SADocument.path == document.get_file_path()).first()
                if doc_instance and doc_instance.hash == document.get_hash():
                    continue
                else:
                    # If the document already exists, drop it
                    if doc_instance:
                        session.delete(doc_instance)
                    # Create the document and add it to the database
                    newdoc = SADocument(path=document.get_file_path(),
                                        hash=document.get_hash(),
                                        date_create=document.get_create_date(),
                                        date_edit=document.get_edit_date(),
                                        date_parse=document.get_parse_date(),
                                        file_size=document.get_file_size(),
                                        num_words=document.get_num_words())
                    session.add(newdoc)

                    # Create a new keyword_instance for each keyword
                    document_kws = document.get_keywords()
                    kws = session.query(SAKeyword).filter(SAKeyword.keyword.in_(document_kws.keys())).all()
                    kws = {kw: document_kws[kw.keyword] for kw in kws}
                    for kw, count in kws.items():
                        kwi = SAKeywordInstance(keyword_id=kw.keyword_id, file_id=newdoc.file_id, count=count
                                                , tag=False)
                        session.add(kwi)
                    session.flush()
            session.commit()
        except Exception as e:
            traceback.print_exc()
            session.rollback()
            raise e
        finally:
            session.close()
        return True

    def get(self, query_text: str):
        """
        Returns any documents that contain the given keyword.
        :param query_text: The text to be queried
        :return: Collection of documents
        """
        return self._get_docs(query_text)

    def _get_docs(self, query: str):
        result = self.db.engine.execute("SELECT * FROM query('%s')"%query)
        ids = [row[0] for row in result]
        docs = self._get_docs_by_id(ids)
        return self._sort_by_id(ids, docs)

    def _get_docs_by_id(self, ids):
        session = self.session()
        q = session.query(SADocument).filter(SADocument.file_id.in_(ids)).all()
        session.close()
        return q

    def _sort_by_id(self, ids, docs):
        doc_map = dict()
        for doc in docs:
            doc_map[doc.file_id] = doc
        r = [doc_map.get(_id) for _id in ids]
        return r

    def get_by_path(self, path: str) -> Document:
        """
        Returns the document associated with a specific file path.
        If there is no Document already stored for that path this will return None.
        :param path: the path of the document
        :return: Document for the path
        """
        session = self.session()

        doc = session.query(SADocument) \
            .filter(SADocument.path == path).first()
        session.close()
        return doc

    # TODO: Implement
    def get_duplicates(self):
        """
        Returns all duplicates that are in this backend.
        The returned map has document hash codes as keys and Collection of all documents with that hash code as values.
        :return: Map of all duplicates found
        """
        pass

    def get_duplicates_of(self, doc: Document):
        """
        Returns all duplicates of the given document.
        It is HIGHLY recommended to override this method for each backend since default implementation gathers all
        duplicates to check.
        If there are no duplicates for the document the returned Collection will be empty.
        :param doc: Document to find duplicates of
        :return: Collection of documents
        """
        session = self.session()

        documents = session.query(SADocument) \
            .filter(SADocument.hash == doc.get_hash()) \
            .filter(SADocument.path != doc.get_file_path())
        return documents

    def remove(self, doc: Document) -> bool:
        session = self.session()
        try:
            doc_instance = session.query(SADocument).filter(SADocument.get_file_path() == doc.get_file_path()).first()
            session.delete(doc_instance)
            session.commit()
        except:
            session.rollback()
            return False
        return True
