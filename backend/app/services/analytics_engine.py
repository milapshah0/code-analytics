from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.commit import Commit
from app.models.jira_issue import JiraIssue
from app.models.merge_request import MergeRequest
from typing import Dict, Any, List
from sqlalchemy import func

class AnalyticsEngine:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_repo_health(self, repo_id: int) -> Dict[str, Any]:
        # Basic stats
        commit_stmt = select(func.count(Commit.id)).where(Commit.repository_id == repo_id)
        commit_count = (await self.db.execute(commit_stmt)).scalar()
        
        mr_stmt = select(func.count(MergeRequest.id)).where(MergeRequest.repository_id == repo_id)
        mr_count = (await self.db.execute(mr_stmt)).scalar()
        
        # Hotspots (frequently changed files - requires shallow clone logic which is pending)
        # For now, return counts
        return {
            "total_commits": commit_count,
            "total_merge_requests": mr_count,
            "risk_score": 0.5 # placeholder
        }

    async def get_correlation_stats(self) -> List[Dict[str, Any]]:
        # Correlate Jira issues with commits
        stmt = select(Commit).where(Commit.jira_key != None)
        commits = (await self.db.execute(stmt)).scalars().all()
        
        correlated = []
        for c in commits:
            stmt = select(JiraIssue).where(JiraIssue.key == c.jira_key)
            issue = (await self.db.execute(stmt)).scalars().first()
            if issue:
                correlated.append({
                    "jira_key": issue.key,
                    "commit_sha": c.sha,
                    "status": issue.status
                })
        return correlated

    async def get_cycle_time_stats(self) -> List[Dict[str, Any]]:
        # Calculate cycle time (Created -> Resolved) for Jira issues
        stmt = select(JiraIssue).where(JiraIssue.resolution_date != None)
        issues = (await self.db.execute(stmt)).scalars().all()
        
        stats = []
        for issue in issues:
            cycle_time = (issue.resolution_date - issue.created_at).days
            stats.append({
                "key": issue.key,
                "cycle_time_days": cycle_time,
                "type": issue.issue_type
            })
        return stats
