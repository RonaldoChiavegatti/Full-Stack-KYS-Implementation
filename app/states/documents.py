import reflex as rx
from sqlmodel import select
import logging
from app.models import Document
from app.states.auth import AuthState
from app.services.storage import StorageService
from app.tasks import process_document_ocr
import random
import string


class DocumentState(rx.State):
    documents: list[Document] = []
    upload_id: str = "upload_area"
    is_uploading: bool = False
    preview_url: str = ""
    preview_text: str = ""
    is_preview_open: bool = False

    @rx.event
    async def load_documents(self):
        """Load user documents from database."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        with rx.session() as session:
            query = (
                select(Document)
                .where(Document.user_id == auth_state.user_id)
                .order_by(Document.created_at.desc())
            )
            self.documents = session.exec(query).all()

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle file upload to MinIO and create DB record."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        storage = StorageService()
        if not storage.is_available:
            yield rx.toast.error(
                "Document storage is currently unavailable. Upload disabled.",
                duration=5000,
                close_button=True,
            )
            return
        self.is_uploading = True
        for file in files:
            try:
                upload_data = await file.read()
                ext = file.name.split(".")[-1]
                random_str = "".join(
                    random.choices(string.ascii_letters + string.digits, k=8)
                )
                unique_filename = f"{auth_state.user_id}/{random_str}_{file.name}"
                storage.upload_file(upload_data, unique_filename, file.content_type)
                with rx.session() as session:
                    new_doc = Document(
                        user_id=auth_state.user_id,
                        filename=file.name,
                        minio_path=unique_filename,
                        file_size=len(upload_data),
                        content_type=file.content_type,
                        status="pending",
                    )
                    session.add(new_doc)
                    session.commit()
                    session.refresh(new_doc)
                    process_document_ocr.delay(new_doc.id)
            except Exception as e:
                logging.exception(f"Upload failed: {e}")
                yield rx.toast.error(f"Failed to upload {file.name}")
        self.is_uploading = False
        yield rx.toast.success("Files uploaded successfully")
        yield DocumentState.load_documents
        return

    @rx.event
    def delete_document(self, doc_id: int, minio_path: str):
        """Delete document from DB and MinIO."""
        try:
            storage = StorageService()
            if storage.is_available:
                storage.delete_file(minio_path)
            with rx.session() as session:
                doc = session.get(Document, doc_id)
                if doc:
                    session.delete(doc)
                    session.commit()
            return DocumentState.load_documents
        except Exception as e:
            logging.exception(f"Delete failed: {e}")
            return rx.toast.error("Failed to delete document")

    @rx.event
    def open_preview(self, doc: Document):
        """Open document preview modal."""
        storage = StorageService()
        if storage.is_available:
            self.preview_url = storage.get_file_url(doc.minio_path)
        else:
            self.preview_url = ""
            yield rx.toast.warning("Storage unavailable. Preview image not loaded.")
        self.preview_text = doc.extracted_text or "No text extracted yet."
        self.is_preview_open = True

    @rx.event
    def close_preview(self):
        self.is_preview_open = False
        self.preview_url = ""
        self.preview_text = ""