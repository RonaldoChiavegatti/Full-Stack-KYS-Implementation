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

        self.internal_endpoint = (
            os.getenv("STORAGE_ENDPOINT")
            or os.getenv("MINIO_ENDPOINT")
            or default_endpoint
        )
        self.public_endpoint = (
            os.getenv("STORAGE_PUBLIC_ENDPOINT")
            or os.getenv("MINIO_PUBLIC_ENDPOINT")
            or "localhost:9000"
        )
        self.bucket_name = os.getenv("STORAGE_BUCKET", "fiscal-documents")

        secure_env = os.getenv("STORAGE_SECURE")
        if secure_env is not None:
            secure = secure_env.lower() == "true"
        else:
            secure = "oraclecloud.com" in self.internal_endpoint
        try:
            self.client = Minio(
                self.internal_endpoint,
                access_key=os.getenv("STORAGE_ACCESS_KEY", os.getenv("MINIO_ACCESS_KEY", "minioadmin")),
                secret_key=os.getenv("STORAGE_SECRET_KEY", os.getenv("MINIO_SECRET_KEY", "minioadmin")),
                secure=secure,
            )
            self._ensure_bucket_exists()
            logging.info(
                f"Storage Service initialized successfully at {self.internal_endpoint}"
            )
        except Exception as e:
            logging.exception(
                f"Storage Service unavailable (Endpoint: {self.internal_endpoint}): {e}"
            )
            self.client = None

    @property
    def is_available(self) -> bool:
        """Check if storage service is initialized and available."""
        return self.client is not None

    def _ensure_bucket_exists(self):
        if not self.client:
            return
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except Exception as e:
            logging.exception(
                f"Error checking/creating bucket '{self.bucket_name}': {e}"
            )

    def upload_file(self, file_data: bytes, filename: str, content_type: str) -> str:
        """Upload a file to MinIO and return the object path."""
        if not self.client:
            raise Exception(
                "Storage service is not available (MinIO client failed to initialize)"
            )
        try:
            self._ensure_bucket_exists()
            file_stream = io.BytesIO(file_data)
            self.client.put_object(
                self.bucket_name,
                filename,
                file_stream,
                length=len(file_data),
                content_type=content_type,
            )
            return filename
        except S3Error as e:
            logging.exception(f"MinIO Upload Error: {e}")
            raise e
        except Exception as e:
            logging.exception(f"Unexpected error during file upload: {e}")
            raise e

    def get_file_url(self, filename: str) -> str:
        """Get a presigned URL for the file."""
        if not self.client:
            logging.error("Storage service unavailable, cannot generate URL")
            return ""
        try:
            url = self.client.get_presigned_url(
                "GET", self.bucket_name, filename, expires=timedelta(hours=1)
            )
            if self.internal_endpoint != self.public_endpoint:
                return url.replace(self.internal_endpoint, self.public_endpoint)
            return url
        except S3Error as e:
            logging.exception(f"MinIO URL Generation Error: {e}")
            return ""
        except Exception as e:
            logging.exception(f"Unexpected error generating file URL: {e}")
            return ""

    def get_file_content(self, filename: str) -> bytes:
        """Download file content from MinIO."""
        if not self.client:
            raise Exception("Storage service unavailable")
        try:
            response = self.client.get_object(self.bucket_name, filename)
            return response.read()
        except Exception as e:
            logging.exception(f"MinIO Download Error: {e}")
            raise e

    def delete_file(self, filename: str):
        """Delete a file from MinIO."""
        if not self.client:
            logging.error("Storage service unavailable, cannot delete file")
            return
        try:
            self.client.remove_object(self.bucket_name, filename)
        except S3Error as e:
            logging.exception(f"MinIO Delete Error: {e}")
        except Exception as e:
            logging.exception(f"Unexpected error during file deletion: {e}")