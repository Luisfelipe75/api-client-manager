from fastapi import APIRouter, Depends
from app.db.mongo import get_db
from app.services.innovasoft_auth import login_remote, register_remote
from app.repositories.session_repo import create_session, delete_session
from app.deps.auth import get_current_user
from app.repositories.operation_repo import log_operation
from app.schemas.auth import LoginRequest, RegisterRequest
from app.utils.validators import validate_password_strength
from app.utils.responses import success_response, error_response
from app.core.logging import logger

router = APIRouter()

@router.post("/login")
async def login(payload: LoginRequest):
    logger.info(f"Intento de login para el usuario: {payload.username}")
    # Validación simple antes de ir al servicio
    if not payload.username or not payload.password:
        logger.warning("Intento de login con campos incompletos")
        return error_response("Campos requeridos", 400)
    
    db = get_db()
    try:
        data = await login_remote(payload.username, payload.password)
        await create_session(db, data['token'], data['userid'], data['username'])
        logger.info(f"Usuario {payload.username} autenticado exitosamente")
        return success_response(data, "Login exitoso")
    except Exception as e:
        logger.error(f"Error durante el login de {payload.username}: {str(e)}")
        return error_response("Credenciales inválidas o error de conexión", 401, str(e))

@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    userid = user['userid']
    db = get_db()
    try:
        await delete_session(db, userid)
        logger.info(f"Sesión cerrada correctamente para UserID: {userid}")
        return success_response(None, "Sesión cerrada correctamente")
    except Exception as e:
        logger.error(f"Error al cerrar sesión para {userid}: {str(e)}")
        return error_response("Error al procesar el cierre de sesión", 500, str(e))

@router.post("/register")
async def register(payload: RegisterRequest):
    db = get_db()
    try:
        if not validate_password_strength(payload.password):
            return error_response(
                "La contraseña debe tener entre 10 y 20 caracteres, incluir mayúsculas, minúsculas y números.",
                400,
            )

        data = await register_remote(payload.username, payload.email, payload.password)
        
        # Si el registro nos devuelve un token, creamos la sesión en nuestra DB
        if data.get('token'):
            await create_session(db, data['token'], data['userid'], data['username'])
            
        # Registramos la operación de creación de usuario exitosa
        await log_operation(db, "REGISTRO", data['username'], data['userid'], 201)
            
        return success_response(data, "Usuario creado correctamente")
    except Exception as e:
        logger.error(f"Error durante el registro del usuario {payload.username}: {str(e)}")
        # Registramos el intento fallido de registro
        await log_operation(db, "REGISTRO", payload.username, "N/A", 400)
        return error_response("Error al procesar el registro del usuario", 400, str(e))
