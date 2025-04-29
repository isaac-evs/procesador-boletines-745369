from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Newsletter(Base):
    __tablename__ = "newsletters"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    email = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Newsletter id={self.id}, email={self.email}, read={self.read}>"
