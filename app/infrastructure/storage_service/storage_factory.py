from app.infrastructure.storage_service.base import StorageInterface
from app.infrastructure.storage_service.s3 import S3Storage


class StorageFactory:
    @staticmethod
    def get_storage_service(storage_type: str, **kwargs) -> StorageInterface:
        if storage_type == 's3':
            return S3Storage(
                aws_access_key_id=kwargs.get('aws_access_key_id'),
                aws_secret_access_key=kwargs.get('aws_secret_access_key')
            )
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")
