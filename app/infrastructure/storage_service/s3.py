from io import BytesIO

import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from typing import List
from app.infrastructure.storage_service.base import StorageInterface
from app.infrastructure.storage_service.schema import FileInfo


class S3Storage(StorageInterface):
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    def list_files(self, bucket: str) -> List[FileInfo]:
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket)
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append(FileInfo(
                        name=obj['Key'],
                        size=str(obj['Size']),
                        type=obj['Key'].split('.')[-1] if '.' in obj['Key'] else 'unknown'
                    ))
            return files
        except (NoCredentialsError, ClientError) as e:
            logging.error(f"Error listing files from S3: {e}")
            raise

    def get_file(self, bucket: str, key: str, download_path: str) -> None:
        try:
            self.s3_client.download_file(bucket, key, download_path)
            logging.info(f"File {key} downloaded from bucket {bucket} to {download_path}.")
        except (NoCredentialsError, ClientError) as e:
            logging.error(f"Error downloading file from S3: {e}")
            raise


