import reflex as rx
import logging
import os
import bcrypt
from datetime import datetime, timedelta
from sqlmodel import SQLModel, create_engine, Session, select
from app.models import User, Billing, Revenue, Document, ChatMessage
from app.pages.landing import landing_page
from app.pages.auth import login_page, register_page
from app.pages.dashboard import dashboard_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
    ],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
    ],
)
from app.pages.documents import documents_page
from app.pages.chat import chat_page
from app.pages.billing import billing_page
from app.pages.profile import profile_page
from app.pages.admin import admin_page
from app.pages.health import health_page
from app.utils.logger import setup_logging

setup_logging()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def init_db():
    """Initialize the database tables and seed initial data."""
    database_url = os.getenv("DATABASE_URL", "sqlite:///reflex.db")
    logging.info(f"Initializing database at {database_url}...")
    try:
        engine = create_engine(database_url)
        SQLModel.metadata.create_all(engine)
        logging.info("Database tables created successfully.")
        with Session(engine) as session:
            try:
                admin_exists = session.exec(
                    select(User).where(User.email == "admin@example.com")
                ).first()
            except Exception as e:
                logging.exception(f"Error checking admin existence: {e}")
                admin_exists = None
            if not admin_exists:
                logging.info("Seeding initial data...")
                admin_user = User(
                    email="admin@example.com",
                    password_hash=hash_password("admin123"),
                    full_name="System Admin",
                    cnpj="00.000.000/0001-99",
                    is_admin=True,
                    created_at=datetime.now(),
                )
                session.add(admin_user)
                test_user = User(
                    email="user@example.com",
                    password_hash=hash_password("user123"),
                    full_name="Maria Silva",
                    cnpj="12.345.678/0001-00",
                    is_admin=False,
                    created_at=datetime.now(),
                )
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                session.refresh(admin_user)
                admin_billing = Billing(
                    user_id=admin_user.id,
                    current_month_tokens=0,
                    total_tokens=0,
                    plan_type="enterprise",
                )
                session.add(admin_billing)
                user_billing = Billing(
                    user_id=test_user.id,
                    current_month_tokens=1500,
                    total_tokens=5000,
                    plan_type="free",
                )
                session.add(user_billing)
                revenues = [
                    {
                        "amount": 2500.0,
                        "description": "Consulting Services - Project A",
                        "category": "Service",
                        "date": (datetime.now() - timedelta(days=5)).strftime(
                            "%Y-%m-%d"
                        ),
                    },
                    {
                        "amount": 1800.0,
                        "description": "Web Development",
                        "category": "Service",
                        "date": (datetime.now() - timedelta(days=15)).strftime(
                            "%Y-%m-%d"
                        ),
                    },
                    {
                        "amount": 450.0,
                        "description": "Product Sales",
                        "category": "Product Sale",
                        "date": (datetime.now() - timedelta(days=20)).strftime(
                            "%Y-%m-%d"
                        ),
                    },
                    {
                        "amount": 3000.0,
                        "description": "Monthly Retainer",
                        "category": "Service",
                        "date": (datetime.now() - timedelta(days=35)).strftime(
                            "%Y-%m-%d"
                        ),
                    },
                ]
                for rev in revenues:
                    revenue_entry = Revenue(
                        user_id=test_user.id,
                        amount=rev["amount"],
                        description=rev["description"],
                        category=rev["category"],
                        date=rev["date"],
                    )
                    session.add(revenue_entry)
                session.commit()
                logging.info("Database seeded successfully.")
            else:
                logging.info("Database already seeded.")
    except Exception as e:
        logging.exception(f"Failed to initialize database: {e}")


app.add_page(landing_page, route="/", title="Fiscal Assistant - MEI")
app.add_page(login_page, route="/login", title="Login - Fiscal Assistant")
app.add_page(register_page, route="/register", title="Register - Fiscal Assistant")
app.add_page(dashboard_page, route="/dashboard", title="Dashboard - Fiscal Assistant")
app.add_page(
    documents_page, route="/dashboard/documents", title="Documents - Fiscal Assistant"
)
app.add_page(
    chat_page, route="/dashboard/chat", title="AI Assistant - Fiscal Assistant"
)
app.add_page(
    billing_page, route="/dashboard/billing", title="Billing - Fiscal Assistant"
)
app.add_page(
    profile_page, route="/dashboard/profile", title="Profile - Fiscal Assistant"
)
app.add_page(admin_page, route="/dashboard/admin", title="Admin - Fiscal Assistant")
app.add_page(
    health_page, route="/dashboard/health", title="System Health - Fiscal Assistant"
)
init_db()