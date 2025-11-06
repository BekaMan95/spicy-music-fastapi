from datetime import datetime
from sqlalchemy import (
    Column, UUID, String, ForeignKey, DateTime, JSON
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Music(Base):
    __tablename__ = "musics"

    _id = Column(UUID, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    album = Column(String(255), nullable=False)
    albumArt = Column(String(255))
    genre = Column(JSON, nullable=False)
    createdAt = Column(DateTime, default=datetime.now())

    # Foreign key to user
    owner_id = Column(UUID, ForeignKey("users._id", ondelete="CASCADE"), nullable=False)

    # Relationship
    owner = relationship("User", back_populates="musics")

    def __repr__(self):
        return f"<Music(title={self.title!r}, artist={self.artist!r})>"
