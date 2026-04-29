from fastapi.responses import JSONResponse
from typing import Any, Optional

def success_response(data: Any = None, message: str = "Operación exitosa", status_code: int = 200):
    """Retorna una respuesta exitosa estandarizada."""
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "data": data
        }
    )

def error_response(message: str = "Ha ocurrido un error", status_code: int = 400, details: Optional[Any] = None):
    """Retorna una respuesta de error estandarizada."""
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "details": details
        }
    )