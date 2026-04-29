from fastapi import APIRouter, Depends, HTTPException
from deps.auth import get_current_user
from db.mongo import get_db
from schemas.client import ClientCreate, ClientUpdate
from services.innovasoft_client import (
    list_clients,
    get_client,
    create_client,
    update_client,
    delete_client,
)
from repositories.operation_repo import log_operation
from utils.files import encode_image_to_base64
from utils.responses import success_response, error_response

router = APIRouter()

@router.post("/listado")
async def search_clients(payload: dict, user=Depends(get_current_user)):
    try:
        payload['usuarioId'] = user['userid']
        data = await list_clients(user['token'], payload)
        return success_response(data, "Listado de clientes recuperado")
    except Exception as e:
        return error_response("Error al listar clientes", 500, str(e))

@router.post("/crear")
async def add_client(payload: ClientCreate, user=Depends(get_current_user)):
    db = get_db()
    try:
        client_data = payload.model_dump()
        client_data['usuarioId'] = user['userid']
        
        # Limpieza de imagen: Si viene con el prefijo Data URI, lo removemos
        if client_data.get("imagen") and "," in client_data["imagen"]:
            client_data["imagen"] = client_data["imagen"].split(",")[1]
            
        resp = await create_client(user['token'], client_data)
        
        status = getattr(resp, 'status_code', 200)
        await log_operation(db, "CREAR", user['username'], client_data.get('identificacion', "N/A"), status)
        
        return success_response(None, "Cliente creado correctamente")
    except Exception as e:
        return error_response("Error al intentar crear el cliente", 400, str(e))


@router.get("/obtener/{client_id}")
async def client_detail(client_id: str, user=Depends(get_current_user)):
    try:
        data = await get_client(user["token"], client_id)
        return success_response(data, "Detalle del cliente obtenido correctamente")
    except Exception as e:
        return error_response("Error al obtener el detalle del cliente", 500, str(e))

@router.post("/actualizar")
async def edit_client(payload: ClientUpdate, user=Depends(get_current_user)):
    db = get_db()
    try:
        client_data = payload.model_dump(exclude_unset=True)
        client_data["usuarioId"] = user["userid"]
        
        # Limpieza de imagen en actualización
        if client_data.get("imagen") and "," in client_data["imagen"]:
            client_data["imagen"] = client_data["imagen"].split(",")[1]
            
        resp = await update_client(user["token"], client_data)
        
        cliente_id = payload.id
        status = getattr(resp, 'status_code', 200)
        await log_operation(db, "ACTUALIZAR", user["username"], cliente_id, status)
        return success_response(None, "Cliente actualizado correctamente")
    except Exception as e:
        cliente_id = payload.id
        await log_operation(db, "ACTUALIZAR", user["username"], cliente_id, 500)
        return error_response("Error al actualizar el cliente", 500,str(e))

@router.delete("/eliminar/{client_id}")
async def remove_client(client_id: str, user=Depends(get_current_user)):
    db = get_db()
    try:
        resp = await delete_client(user["token"], client_id)
        status = getattr(resp, 'status_code', 200)
        await log_operation(db, "ELIMINAR", user["username"], client_id, status)
        return success_response(None, "Cliente eliminado correctamente")
    except Exception as e:
        await log_operation(db, "ELIMINAR", user["username"], client_id, 500)
        return error_response("Error al eliminar el cliente", 500, str(e))