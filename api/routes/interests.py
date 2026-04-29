from fastapi import APIRouter, Depends, HTTPException
from app.services.innovasoft_interest import list_interests
from app.deps.auth import get_current_user

router = APIRouter()

@router.get("/listado")
async def get_interests(user=Depends(get_current_user)):
    try:
        return await list_interests(user['token'])
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener intereses")
    