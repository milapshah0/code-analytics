from sqlalchemy import String, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base

class JiraIssue(Base):
    __tablename__ = "jira_issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    summary: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(100))
    issue_type: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str | None] = mapped_column(String(50))
    assignee: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    resolution_date: Mapped[datetime | None] = mapped_column(DateTime)
    
    # Process history
    status_history: Mapped[list | None] = mapped_column(JSON)
