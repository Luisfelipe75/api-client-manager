import httpx
from core.config import settings

async def list_interests(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
        resp = await client.get("api/Intereses/Listado", headers=headers)
        resp.raise_for_status()
        return resp.json()
    