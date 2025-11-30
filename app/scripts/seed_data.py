import logging
import os
import sys
import bcrypt
from datetime import datetime, timedelta
from sqlmodel import Session, create_engine, select
from app.models import User, Revenue, Billing, Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_data():
    """Seed the database with initial test data."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable is not set.")
        sys.exit(1)
    engine = create_engine(database_url)
    with Session(engine) as session:
        logger.info("Checking for existing data...")
        admin_exists = session.exec(
            select(User).where(User.email == "admin@example.com")
        ).first()
        if admin_exists:
            logger.info("Data already seeded. Skipping.")
            return
        logger.info("Seeding data...")
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
                "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            },
            {
                "amount": 1800.0,
                "description": "Web Development",
                "category": "Service",
                "date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
            },
            {
                "amount": 450.0,
                "description": "Product Sales",
                "category": "Product Sale",
                "date": (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"),
            },
            {
                "amount": 3000.0,
                "description": "Monthly Retainer",
                "category": "Service",
                "date": (datetime.now() - timedelta(days=35)).strftime("%Y-%m-%d"),
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
        logger.info("Database seeded successfully!")
        logger.info("Admin: admin@example.com / admin123")
        logger.info("User: user@example.com / user123")


if __name__ == "__main__":
    seed_data()