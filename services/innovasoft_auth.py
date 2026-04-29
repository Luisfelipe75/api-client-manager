import httpx
from core.config import settings

async def login_remote(username: str, password: str):
    async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
        resp = await client.post("api/Authenticate/login", json={
            "username": username, 
            "password": password
        })
        resp.raise_for_status()
        raw_data = resp.json()
        
        # Extraemos los datos manejando posibles variaciones en los nombres de campos
        # Si la API externa usa 'accessToken' o 'userId', aquí los estandarizamos
        return {
            "token": raw_data.get("token") or raw_data.get("accessToken") or raw_data.get("tokenValue"),
            "userid": str(raw_data.get("userid") or raw_data.get("userId") or raw_data.get("id") or ""),
            "username": raw_data.get("username") or raw_data.get("userName") or username
        }

async def register_remote(username: str, email: str, password: str):
    async with httpx.AsyncClient(base_url=settings.api_base_url, timeout=30) as client:
        resp = await client.post("api/Authenticate/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        resp.raise_for_status()
        raw_data = resp.json()
        return {
            "token": raw_data.get("token") or raw_data.get("accessToken"),
            "userid": str(raw_data.get("userid") or raw_data.get("userId") or raw_data.get("id") or ""),
            "username": raw_data.get("username") or username,
            "email": email
        }
    