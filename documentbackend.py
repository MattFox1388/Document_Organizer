from abc import ABC, abstractmethod
from typing import List

from document import TDocument


class TDocumentBackend(type):
    pass


class DocumentBackend(ABC, TDocumentBackend):

    @abstractmethod
    def store(self, doc: TDocument) -> bool:
        pass

    def get(self, keyword: str) -> List[TDocument]:
        pass
