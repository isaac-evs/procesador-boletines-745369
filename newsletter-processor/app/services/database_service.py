from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from app.config import DATABASE_URL
from app.models.newsletter import Base, Newsletter

logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def get_db_session():
    session = SessionLocal()
    try:
        return session
    finally:
        session.close()

def save_newsletter(content, email, image_url):
    try:
        session = get_db_session()
        newsletter = Newsletter(
            content=content,
            email=email,
            image_url=image_url,
            read=False
        )

        session.add(newsletter)
        session.commit()
        session.refresh(newsletter)

        logger.info(f"Newsletter saved to database with ID: {newsletter.id}")
        return newsletter

    except Exception as e:
        logger.error(f"Error saving newsletter to database: {e}")
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()
