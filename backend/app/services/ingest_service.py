import re
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.repo import Repository
from app.models.commit import Commit
from app.models.merge_request import MergeRequest
from app.models.jira_issue import JiraIssue
from app.services.gitlab_client import GitLabClient
from app.services.jira_client import JiraClient
from datetime import datetime

class IngestService:
    def __init__(self, db: AsyncSession, gitlab_client: GitLabClient, jira_client: JiraClient):
        self.db = db
        self.gl = gitlab_client
        self.jr = jira_client

    def _extract_jira_key(self, text: str) -> str | None:
        if not text:
            return None
        match = re.search(r'([A-Z]+-\d+)', text)
        return match.group(1) if match else None

    async def sync_gitlab_projects(self, group_id: int | None = None):
        if group_id:
            projects = await self.gl.get_group_projects(group_id)
        else:
            projects = await self.gl.get_projects()
        
        for p in projects:
            stmt = select(Repository).where(Repository.gitlab_id == p['id'])
            result = await self.db.execute(stmt)
            repo = result.scalars().first()
            
            if not repo:
                repo = Repository(
                    gitlab_id=p['id'],
                    name=p['name'],
                    path_with_namespace=p['path_with_namespace'],
                    url=p['web_url'],
                    created_at=datetime.fromisoformat(p['created_at'].replace('Z', '+00:00'))
                )
                self.db.add(repo)
        
        await self.db.commit()

    async def sync_project_data(self, project_id: int):
        # 1. Sync Commits
        commits = await self.gl.get_project_commits(project_id)
        repo_stmt = select(Repository).where(Repository.gitlab_id == project_id)
        repo_res = await self.db.execute(repo_stmt)
        repo = repo_res.scalars().first()
        
        if not repo:
            return

        for c in commits:
            stmt = select(Commit).where(Commit.sha == c['id'])
            res = await self.db.execute(stmt)
            if not res.scalars().first():
                jira_key = self._extract_jira_key(c['message'])
                new_commit = Commit(
                    sha=c['id'],
                    message=c['message'],
                    author_name=c['author_name'],
                    author_email=c['author_email'],
                    authored_date=datetime.fromisoformat(c['authored_date'].replace('Z', '+00:00')),
                    repository_id=repo.id,
                    jira_key=jira_key
                )
                self.db.add(new_commit)

        # 2. Sync Merge Requests
        mrs = await self.gl.get_merge_requests(project_id)
        for mr in mrs:
            stmt = select(MergeRequest).where(MergeRequest.gitlab_id == mr['id'])
            res = await self.db.execute(stmt)
            if not res.scalars().first():
                jira_key = self._extract_jira_key(mr['title'])
                new_mr = MergeRequest(
                    gitlab_id=mr['id'],
                    iid=mr['iid'],
                    title=mr['title'],
                    state=mr['state'],
                    author_name=mr['author']['name'],
                    created_at=datetime.fromisoformat(mr['created_at'].replace('Z', '+00:00')),
                    merged_at=datetime.fromisoformat(mr['merged_at'].replace('Z', '+00:00')) if mr['merged_at'] else None,
                    repository_id=repo.id,
                    jira_key=jira_key
                )
                self.db.add(new_mr)

        await self.db.commit()

    async def sync_jira_issues(self, project_key: str):
        issues = await self.jr.get_project_issues(project_key)
        for issue_data in issues:
            stmt = select(JiraIssue).where(JiraIssue.key == issue_data['key'])
            res = await self.db.execute(stmt)
            issue = res.scalars().first()
            
            fields = issue_data['fields']
            created = datetime.fromisoformat(fields['created'].replace('Z', '+00:00'))
            updated = datetime.fromisoformat(fields['updated'].replace('Z', '+00:00'))
            resolved = datetime.fromisoformat(fields['resolutiondate'].replace('Z', '+00:00')) if fields.get('resolutiondate') else None
            
            if not issue:
                issue = JiraIssue(
                    key=issue_data['key'],
                    summary=fields['summary'],
                    status=fields['status']['name'],
                    issue_type=fields['issuetype']['name'],
                    priority=fields.get('priority', {}).get('name'),
                    assignee=fields.get('assignee', {}).get('displayName'),
                    created_at=created,
                    updated_at=updated,
                    resolution_date=resolved,
                    status_history=issue_data.get('changelog', {}).get('histories', [])
                )
                self.db.add(issue)
            else:
                issue.summary = fields['summary']
                issue.status = fields['status']['name']
                issue.assignee = fields.get('assignee', {}).get('displayName')
                issue.updated_at = updated
                issue.resolution_date = resolved
                issue.status_history = issue_data.get('changelog', {}).get('histories', [])
        
        await self.db.commit()
