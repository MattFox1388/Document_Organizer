from abc import abstractmethod, ABC
from typing import Collection


class StorageBackend(ABC):

    @abstractmethod
    def get(self, query: str) -> Collection[str]:
        pass