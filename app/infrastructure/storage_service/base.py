from abc import ABC, abstractmethod
from typing import List

from app.infrastructure.storage_service.schema import FileInfo


class StorageInterface(ABC):

    @abstractmethod
    def list_files(self, bucket: str) -> List[FileInfo]:
        pass

    @abstractmethod
    def get_file(self, bucket: str, key: str, download_path: str) -> None:
        pass

