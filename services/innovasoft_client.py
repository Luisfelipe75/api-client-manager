import httpx
from app.core.config import settings

async def list_clients(token: str, payload: dict):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
        resp = await client.post("api/Cliente/Listado", json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()

async def get_client(token: str, client_id: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
        resp = await client.get(f"api/Cliente/Obtener/{client_id}", headers=headers)
        resp.raise_for_status()
        return resp.json()

async def create_client(token: str, payload: dict):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
        resp = await client.post("api/Cliente/Crear", json=payload, headers=headers)
        resp.raise_for_status()
        return resp

async def update_client(token: str, payload: dict):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
        resp = await client.post("api/Cliente/Actualizar", json=payload, headers=headers)
        resp.raise_for_status()
        return resp

async def delete_client(token: str, client_id: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
        resp = await client.delete(f"api/Cliente/Eliminar/{client_id}", headers=headers)
        resp.raise_for_status()
        return resp
    