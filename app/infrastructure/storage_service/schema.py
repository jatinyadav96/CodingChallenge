from enum import Enum
from pydantic import BaseModel


class StorageType(str, Enum):
    S3 = "S3"


class FileInfo(BaseModel):
    name: str
    size: str
    type: str
