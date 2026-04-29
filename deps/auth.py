from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.mongo import get_db
from repositories.session_repo import get_session_by_token

bearer_scheme = HTTPBearer(auto_error=False)

async def get_token_credentials(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
        )
    return credentials.credentials

async def get_current_session(
    token: str = Depends(get_token_credentials),
):
    db = get_db()
    session = await get_session_by_token(db, token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada",
        )
    return session

async def get_current_user(
    session: dict = Depends(get_current_session),
):
    return {
        "userid": session["userid"],
        "username": session["username"],
        "token": session["token"],
        "login_timestamp": session["login_timestamp"],
    }