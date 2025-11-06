from datetime import datetime
from sqlalchemy import (
    Column, UUID, String, DateTime, Boolean
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    _id = Column(UUID, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    profilePic = Column(String(255))
    createdAt = Column(DateTime, default=datetime.now())

    # Relationship
    musics = relationship("Music", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username={self.username!r}, email={self.email!r})>"

