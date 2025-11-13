from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from src.config import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid



class User(Base):
    __tablename__ = "users"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    profilePic = Column(String(255))
    createdAt = Column(DateTime, default=datetime.now)

    # Relationship
    musics = relationship("Music", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username={self.username!r}, email={self.email!r})>"

