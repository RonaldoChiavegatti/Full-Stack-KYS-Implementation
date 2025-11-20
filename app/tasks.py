import reflex as rx
from app.celery_app import celery_app
from app.models import Document
from app.services.storage import StorageService
from sqlmodel import Session, create_engine, select
import pytesseract
from PIL import Image
import io
import os
import logging

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reflex.db")
engine = create_engine(DATABASE_URL)


@celery_app.task(name="app.tasks.process_document_ocr")
def process_document_ocr(document_id: int):
    """Background task to process OCR for a document."""
    storage = StorageService()
    with Session(engine) as session:
        document = session.get(Document, document_id)
        if not document:
            logging.error(f"Document {document_id} not found")
            return
        try:
            document.status = "processing"
            session.add(document)
            session.commit()
            file_data = storage.get_file_content(document.minio_path)
            image = Image.open(io.BytesIO(file_data))
            text = pytesseract.image_to_string(image)
            document.extracted_text = text
            document.status = "completed"
            session.add(document)
            session.commit()
        except Exception as e:
            logging.exception(f"OCR Processing failed for document {document_id}: {e}")
            document.status = "failed"
            session.add(document)
            session.commit()