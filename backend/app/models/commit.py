from sqlalchemy import String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base

class Commit(Base):
    __tablename__ = "commits"

    id: Mapped[int] = mapped_column(primary_key=True)
    sha: Mapped[str] = mapped_column(String(100), unique=True)
    message: Mapped[str] = mapped_column(String)
    author_name: Mapped[str] = mapped_column(String(255))
    author_email: Mapped[str] = mapped_column(String(255))
    authored_date: Mapped[datetime] = mapped_column(DateTime)
    
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"))
    repository = relationship("Repository", back_populates="commits")
    
    # Correlation field
    jira_key: Mapped[str | None] = mapped_column(String(50), index=True)
    
    # Analytics data
    stats: Mapped[dict | None] = mapped_column(JSON) # lines added/removed etc.
