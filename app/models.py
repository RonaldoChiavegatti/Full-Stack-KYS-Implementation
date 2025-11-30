import reflex as rx
from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    """User model for authentication and profile."""

    id: int | None = Field(default=None, primary_key=True)
    email: str
    password_hash: str
    full_name: str
    cnpj: str = ""
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


class Billing(SQLModel, table=True):
    """Billing model for tracking usage."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    current_month_tokens: int = 0
    total_tokens: int = 0
    plan_type: str = "free"
    last_updated: datetime = Field(default_factory=datetime.now)


class Revenue(SQLModel, table=True):
    """Revenue model for tracking income."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    amount: float
    description: str
    category: str
    date: str
    created_at: datetime = Field(default_factory=datetime.now)


class Document(SQLModel, table=True):
    """Document model for stored files and OCR data."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    filename: str
    minio_path: str
    file_size: int
    content_type: str
    status: str = "pending"
    extracted_text: str | None = Field(
        default=None, sa_column_kwargs={"nullable": True}
    )
    created_at: datetime = Field(default_factory=datetime.now)


class ChatMessage(SQLModel, table=True):
    """Model for storing chat history."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    role: str
    content: str = Field(sa_column_kwargs={"nullable": False})
    tokens_used: int = 0
    created_at: datetime = Field(default_factory=datetime.now)