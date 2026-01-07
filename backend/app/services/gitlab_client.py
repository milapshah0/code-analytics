import httpx
from typing import List, Dict, Any
from app.database import settings

class GitLabClient:
    def __init__(self, token: str, base_url: str = "https://gitlab.com/api/v4"):
        self.token = token
        self.base_url = base_url
        self.headers = {"PRIVATE-TOKEN": self.token}

    async def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_projects(self) -> List[Dict[str, Any]]:
        return await self._get("projects", params={"membership": True, "simple": True})

    async def get_group_projects(self, group_id: int) -> List[Dict[str, Any]]:
        return await self._get(f"groups/{group_id}/projects", params={"include_subgroups": True, "simple": True})

    async def get_project_commits(self, project_id: int, ref_name: str = "main") -> List[Dict[str, Any]]:
        return await self._get(f"projects/{project_id}/repository/commits", params={"ref_name": ref_name})

    async def get_merge_requests(self, project_id: int) -> List[Dict[str, Any]]:
        return await self._get(f"projects/{project_id}/merge_requests")

    async def get_commit_details(self, project_id: int, sha: str) -> Dict[str, Any]:
        return await self._get(f"projects/{project_id}/repository/commits/{sha}")
