import short_url

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User


class WorkspaceOpenManager:

    @staticmethod
    async def create_open_url(workspace_id: int):
        url = short_url.encode_url(workspace_id)
        return url

    @staticmethod
    async def get_workspace_id(workspace_open_url):
        workspace_id = short_url.decode_url(workspace_open_url)
        return workspace_id
