from pydantic import BaseModel, Field
from typing import Optional

class ClientBase(BaseModel):
    nombre: str = Field(..., max_length=50)
    apellidos: str = Field(..., max_length=100)
    identificacion: str = Field(..., max_length=20)
    celular: str = Field(..., max_length=20)
    otroTelefono: Optional[str] = Field(None, max_length=20)
    direccion: str = Field(..., max_length=200)
    fNacimiento: str
    fAfiliacion: str
    sexo: str = Field(..., max_length=1)
    resennaPersonal: str = Field(..., max_length=200)
    imagen: Optional[str] = None
    interesFK: str
    usuarioId: str


class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    id: str  # El ID es obligatorio para saber qué cliente editar
    nombre: Optional[str] = Field(None, max_length=50)
    apellidos: Optional[str] = Field(None, max_length=100)
    identificacion: Optional[str] = Field(None, max_length=20)
    celular: Optional[str] = Field(None, max_length=20)
    otroTelefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    fNacimiento: Optional[str] = None
    fAfiliacion: Optional[str] = None
    sexo: Optional[str] = Field(None, max_length=1)
    resennaPersonal: Optional[str] = Field(None, max_length=200)
    imagen: Optional[str] = None
    interesFK: Optional[str] = None
    usuarioId: Optional[str] = None