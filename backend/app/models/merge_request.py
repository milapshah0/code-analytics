from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base

class MergeRequest(Base):
    __tablename__ = "merge_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    gitlab_id: Mapped[int] = mapped_column(unique=True)
    iid: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column(String(500))
    state: Mapped[str] = mapped_column(String(50))
    author_name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    merged_at: Mapped[datetime | None] = mapped_column(DateTime)
    
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"))
    repository = relationship("Repository", back_populates="merge_requests")
    
    jira_key: Mapped[str | None] = mapped_column(String(50), index=True)
