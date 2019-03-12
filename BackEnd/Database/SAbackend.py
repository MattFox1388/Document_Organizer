from .SAKeywordInstance import SAKeywordInstance
from .SAKeyword import SAKeyword
from .SADocument import SADocument
from BackEnd.Documents import Document
from BackEnd.Documents import DocumentBackend
from typing import Collection, Mapping
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SABackend(DocumentBackend):
    db = None
    session = None

    def __new__(cls, host: str, dbname: str, user: str, password: str, port: str):
        return super(SABackend, cls).__new__(cls)

    def __init__(self, host: str, dbname: str, user: str, password: str, port: str):
        # Open connection
        database = "postgresql+psycopg2://%s:%s@%s:%s/%s"%(
            user, password, host, port, dbname)
        self.db = create_engine(database)
        self.session = sessionmaker(self.db)

    def close(self):
        """
        Frees all hardware resources that this backend uses.
        As sessions are made per method, nothing should need to be closed.
        :return: None
        """
        return

    def store(self, docs: Collection[Document]) -> bool:
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
                    instance = session.query(SAKeyword).filter(SAKeyword.keyword == kw.keyword).first()
                    if instance:
                        kw = instance
                    else:
                        session.add(kw)
                session.flush()

                # Check to see if the document exists and if the hash matches
                doc_instance = session.query(SADocument).filter(SADocument.path == document.get_file_path()).first()
                if doc_instance and doc_instance.hash == document.get_hash():
                    continue
                else:
                    # If the document already exists, drop it
                    if doc_instance:
                        session.delete(doc_instance)
                        session.flush()
                    # Create the document and add it to the database
                    newdoc = SADocument(path=document.get_file_path(),
                                        hash=document.get_hash(),
                                        date_create=document.get_create_date(),
                                        date_edit=document.get_edit_date(),
                                        date_parse=document.get_parse_date())
                    session.add(newdoc)
                    session.flush()

                    # Create a new keyword_instance for each keyword
                    document_kws = document.get_keywords()
                    kws = session.query(SAKeyword).filter(SAKeyword.keyword.in_(document_kws.keys())).all()
                    kws = {kw: document_kws[kw.keyword] for kw in kws}
                    for kw, count in kws.items():
                        kwi = SAKeywordInstance(keyword_id=kw.keyword_id, file_id=newdoc.file_id, count=count)
                        session.add(kwi)
                    session.flush()
            session.commit()
        except:
            session.rollback()
            return False
        return True

    def get(self, keyword: str) -> Collection[Document]:
        """
        Returns any documents that contain the given keyword.
        :param keyword: The keyword in question
        :return: Collection of documents
        """
        session = self.session()

        documents = session.query(SADocument)\
            .filter(SADocument.instance.keyword.in_(keyword)).all()
        return documents

    def get_by_path(self, path: str) -> Document:
        """
        Returns the document associated with a specific file path.
        If there is no Document already stored for that path this will return None.
        :param path: the path of the document
        :return: Document for the path
        """
        session = self.session()

        documents = session.query(SADocument)\
            .filter(SADocument.path == path).all()
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

        documents = session.query(SADocument)\
            .filter(SADocument.hash == doc.get_hash())\
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
