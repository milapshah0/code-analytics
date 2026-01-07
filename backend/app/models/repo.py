from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True)
    gitlab_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(255))
    path_with_namespace: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    commits = relationship("Commit", back_populates="repository", cascade="all, delete-orphan")
    merge_requests = relationship("MergeRequest", back_populates="repository", cascade="all, delete-orphan")
