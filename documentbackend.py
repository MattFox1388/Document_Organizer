from abc import ABC, abstractmethod
from typing import List, Collection, Mapping

from document import TDocument, Document


class TDocumentBackend(type):
    pass


class DocumentBackend(ABC, TDocumentBackend):

    @abstractmethod
    def store(self, docs: Collection[TDocument]) -> bool:
        """
        Stores multiple documents into this backend that can be retrieved later.
        :param docs: A collection of documents that will be stored.
        :return: True if documents were stored successfully, False otherwise.
        """
        pass

    @abstractmethod
    def get(self, keyword: str) -> Collection[TDocument]:
        """
        Returns any documents that contain the given keyword.
        :param keyword: The keyword in question
        :return: Collection of documents
        """
        pass

    @abstractmethod
    def get_duplicates(self) -> Mapping[int,Collection[TDocument]]:
        """
        Returns all duplicates that are in this backend.
        The returned map has document hash codes as keys and Collection of all documents with that hash code as values.
        :return: Map of all duplicates found
        """
        pass

    def get_duplicates_of(self, doc: TDocument) -> Collection[TDocument]:
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
