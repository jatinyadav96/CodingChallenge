import logging
import os

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

from app.core.config import settings
from app.domain.drawing.drawing_service import DrawingService
from app.infrastructure.storage_service.storage_factory import StorageFactory

router = APIRouter()

storage_service = StorageFactory.get_storage_service(
    storage_type='s3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

drawing_service = DrawingService(storage_service=storage_service)
MAX_FILE_SIZE_MB = 50
ALLOWED_FILE_TYPES = {'pdf', 'tiff', 'jpeg', 'png'}


@router.get("")
async def list_drawings():
    try:
        bucket = settings.BUCKET_NAME
        files = drawing_service.list_drawings(bucket)
        return {"drawings": files}
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing drawings: {e}")


@router.get("/{key}")
async def get_drawing(key: str):
    try:
        download_path = f"/tmp/{key}"
        bucket = settings.BUCKET_NAME
        drawing_service.get_drawing(bucket, key, download_path)

        file_size_mb = os.path.getsize(download_path) / (1024 * 1024)
        file_type = key.split('.')[-1].lower()

        if file_size_mb > MAX_FILE_SIZE_MB:
            os.remove(download_path)
            raise HTTPException(status_code=413, detail="File too large")

        if file_type not in ALLOWED_FILE_TYPES:
            os.remove(download_path)
            raise HTTPException(status_code=415, detail="Unsupported file type")

        return FileResponse(path=download_path)
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error downloading drawing: {e}")

