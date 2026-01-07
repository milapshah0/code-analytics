import httpx
from typing import List, Dict, Any
from app.database import settings

class JiraClient:
    def __init__(self, url: str, email: str, token: str):
        self.url = url.rstrip('/')
        self.auth = (email, token)

    async def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/rest/api/3/{endpoint}",
                auth=self.auth,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_issue(self, key: str) -> Dict[str, Any]:
        return await self._get(f"issue/{key}")

    async def search_issues(self, jql: str) -> Dict[str, Any]:
        return await self._get("search", params={"jql": jql, "expand": "changelog"})

    async def get_project_issues(self, project_key: str) -> List[Dict[str, Any]]:
        result = await self.search_issues(f"project = {project_key}")
        return result.get('issues', [])
