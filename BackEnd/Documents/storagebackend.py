import math
from abc import ABC, abstractmethod

from document import Document


class StorageBackend(ABC):

    @abstractmethod
    def get_total_document_count(self) -> int:
        pass

    def _get_inverse_document_frequncy(self, docs_with_term) -> float:
        if not docs_with_term:
            return 0
        return math.log(self.get_total_document_count() / len(docs_with_term))

    @staticmethod
    def _get_relevance(doc: Document, term: str, idf: float) -> float:
        return doc.get_term_frequency(term) * idf

    @abstractmethod
    def close(self):
        """
        Frees all hardware resources that this backend uses.
        :return: None
        """
        pass

    @abstractmethod
    def store(self, docs) -> bool:
        """
        Stores multiple documents into this backend that can be retrieved later.
        :param docs: A collection of documents that will be stored.
        :return: True if documents were stored successfully, False otherwise.
        """
        pass

    @abstractmethod
    def get(self, keyword: str):
        """
        Returns any documents that contain the given keyword.
        :param keyword: The keyword in question
        :return: Collection of documents
        """
        pass

    @abstractmethod
    def get_by_path(self, path: str) -> Document:
        """
        Returns the document associated with a specific file path.
        If there is no Document already stored for that path this will return None.
        :param path: the path of the document
        :return: Document for the path
        """
        pass

    @abstractmethod
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
        dupes = self.get_duplicates()
        hash = doc.get_hash()
        if hash in dupes:
            return dupes[hash]
        return []

    @abstractmethod
    def remove(self, doc: Document) -> bool:
        pass
