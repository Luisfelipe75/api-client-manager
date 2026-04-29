from datetime import datetime, timezone
from db.collections import CollectionNames

async def log_operation(db, accion: str, usuario: str, cliente_id: str, resultado: int):
    await db[CollectionNames.OPERACIONES].insert_one({
        "accion": accion,
        "usuario": usuario,
        "cliente_id": cliente_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resultado": resultado
    })