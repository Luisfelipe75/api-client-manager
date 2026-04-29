from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongo import connect_mongo, close_mongo
from app.api.router import api_router
from app.core.logging import logger
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicio: Conexión a la base de datos
    logger.info("Conectando a los servicios de datos...")
    await connect_mongo()
    logger.info("API local iniciada y lista para recibir peticiones")
    yield
    # Cierre: Limpieza de recursos
    logger.info("Cerrando recursos de la API...")
    await close_mongo()
    logger.info("API local detenida correctamente")

app = FastAPI(title=settings.app_name, lifespan=lifespan)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origins] if settings.cors_origins == "*" else settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de rutas modularizadas
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

