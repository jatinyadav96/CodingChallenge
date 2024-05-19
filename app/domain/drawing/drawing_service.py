from typing import List
from app.infrastructure.storage_service.base import StorageInterface
from app.infrastructure.storage_service.schema import FileInfo


class DrawingService:
    def __init__(self, storage_service: StorageInterface):
        self.storage_service = storage_service

    def list_drawings(self, bucket: str) -> List[FileInfo]:
        return self.storage_service.list_files(bucket)

    def get_drawing(self, bucket: str, key: str, download_path: str) -> None:
        self.storage_service.get_file(bucket, key, download_path)
