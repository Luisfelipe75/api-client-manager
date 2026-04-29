from pydantic import BaseModel

class InterestResponse(BaseModel):
    id: str
    descripcion: str