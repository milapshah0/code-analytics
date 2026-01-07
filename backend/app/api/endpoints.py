from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.analytics_engine import AnalyticsEngine
from app.services.ingest_service import IngestService
from app.services.gitlab_client import GitLabClient
from app.services.jira_client import JiraClient
import os

router = APIRouter()

def get_services(db: AsyncSession = Depends(get_db)):
    gl = GitLabClient(token=os.getenv("GITLAB_TOKEN", ""))
    jr = JiraClient(
        url=os.getenv("JIRA_URL", ""),
        email=os.getenv("JIRA_EMAIL", ""),
        token=os.getenv("JIRA_TOKEN", "")
    )
    ingest = IngestService(db, gl, jr)
    analytics = AnalyticsEngine(db)
    return {"ingest": ingest, "analytics": analytics}

@router.get("/repos/{repo_id}/health")
async def get_repo_health(repo_id: int, services: dict = Depends(get_services)):
    return await services["analytics"].get_repo_health(repo_id)

@router.get("/analytics/correlations")
async def get_correlations(services: dict = Depends(get_services)):
    return await services["analytics"].get_correlation_stats()

@router.get("/analytics/cycle-time")
async def get_cycle_time(services: dict = Depends(get_services)):
    return await services["analytics"].get_cycle_time_stats()

@router.post("/scan/gitlab")
async def trigger_gitlab_scan(services: dict = Depends(get_services)):
    from app.database import settings
    await services["ingest"].sync_gitlab_projects(group_id=settings.GITLAB_GROUP_ID)
    return {"status": "scan initiated"}

@router.post("/scan/jira/{project_key}")
async def trigger_jira_scan(project_key: str, services: dict = Depends(get_services)):
    await services["ingest"].sync_jira_issues(project_key)
    return {"status": "scan initiated"}
