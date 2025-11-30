import os
from minio import Minio
from minio.error import S3Error
import io
import logging
from datetime import timedelta


class StorageService:
    def __init__(self):
        default_endpoint = "localhost:9000"
        if os.path.exists("/.dockerenv"):
            default_endpoint = "minio:9000"
        self.internal_endpoint = os.getenv("MINIO_ENDPOINT", default_endpoint)
        self.public_endpoint = os.getenv("MINIO_PUBLIC_ENDPOINT", "localhost:9000")
        self.bucket_name = "fiscal-documents"
        self.client = None
        try:
            client = Minio(
                self.internal_endpoint,
                access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
                secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
                secure=False,
            )
            if not client.bucket_exists(self.bucket_name):
                client.make_bucket(self.bucket_name)
            self.client = client
            logging.info(
                f"Storage Service initialized successfully at {self.internal_endpoint}"
            )
        except Exception as e:
            logging.exception(
                f"Storage Service unavailable (Endpoint: {self.internal_endpoint}). Document features will be limited. Error: {e}"
            )
            logging.info(
                "To enable storage, ensure MinIO is running and accessible via MINIO_ENDPOINT."
            )
            self.client = None

    @property
    def is_available(self) -> bool:
        """Check if storage service is initialized and available."""
        return self.client is not None

    def upload_file(self, file_data: bytes, filename: str, content_type: str) -> str:
        """Upload a file to MinIO and return the object path."""
        if not self.is_available:
            raise Exception("Storage service is not available. Cannot upload file.")
        try:
            file_stream = io.BytesIO(file_data)
            self.client.put_object(
                self.bucket_name,
                filename,
                file_stream,
                length=len(file_data),
                content_type=content_type,
            )
            return filename
        except Exception as e:
            logging.exception(f"Storage Upload Error: {e}")
            raise e

    def get_file_url(self, filename: str) -> str:
        """Get a presigned URL for the file."""
        if not self.is_available:
            logging.warning("Storage service unavailable, cannot generate URL")
            return ""
        try:
            url = self.client.get_presigned_url(
                "GET", self.bucket_name, filename, expires=timedelta(hours=1)
            )
            if self.internal_endpoint != self.public_endpoint:
                return url.replace(self.internal_endpoint, self.public_endpoint)
            return url
        except Exception as e:
            logging.exception(f"Storage URL Generation Error: {e}")
            return ""

    def get_file_content(self, filename: str) -> bytes:
        """Download file content from MinIO."""
        if not self.is_available:
            raise Exception("Storage service unavailable. Cannot download file.")
        try:
            response = self.client.get_object(self.bucket_name, filename)
            return response.read()
        except Exception as e:
            logging.exception(f"Storage Download Error: {e}")
            raise e

    def delete_file(self, filename: str):
        """Delete a file from MinIO."""
        if not self.is_available:
            return
        try:
            self.client.remove_object(self.bucket_name, filename)
        except Exception as e:
            logging.exception(f"Storage Delete Error: {e}")