import logging
import os
import sys
from sqlmodel import SQLModel, create_engine
from app.models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize the database tables."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable is not set.")
        sys.exit(1)
    logger.info(f"Connecting to database...")
    try:
        engine = create_engine(database_url)
        logger.info("Creating tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database initialization completed successfully.")
    except Exception as e:
        logger.exception(f"Failed to initialize database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_db()