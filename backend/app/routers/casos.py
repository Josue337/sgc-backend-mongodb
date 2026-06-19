from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_database, get_next_sequence_value
from app.schemas.caso import CasoCreate, CasoUpdate, CasoResponse
from typing import List

from app.routers.users import obtener_usuario_actual

router = APIRouter(
    prefix="/casos",
    tags=["Casos"]
)

@router.post("/", response_model=CasoResponse, status_code=status.HTTP_201_CREATED)
async def crear_caso(caso: CasoCreate, db = Depends(get_database)):
    # 1. Verificar si ya existe un caso con ese ID
    caso_existente = await db["casos"].find_one({"id_caso": caso.id_caso})
    if caso_existente:
        raise HTTPException(
            status_code=400, 
            detail=f"El caso con id_caso {caso.id_caso} ya existe."
        )
    
    # 2. Convertir el esquema de Pydantic a diccionario e inyectar fecha por defecto
    nuevo_caso = caso.model_dump()
    nuevo_caso["fecha_creacion"] = nuevo_caso.get("fecha_creacion") or datetime.utcnow()
    nuevo_caso["activo"] = True
    
    # 3. Insertar en MongoDB
    try:
        await db["casos"].insert_one(nuevo_caso)
        return nuevo_caso
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar en la DB: {e}")


@router.get("/", response_model=List[CasoResponse])
async def obtener_casos(skip: int = 0, limit: int = 50, db = Depends(get_database)):
    # Buscamos solo los casos activos para el listado general
    cursor = db["casos"].find({"activo": True}).skip(skip).limit(limit)
    casos = await cursor.to_list(length=limit)
    return casos


@router.get("/audit/logs", status_code=status.HTTP_200_OK)
async def obtener_historial_auditoria(db = Depends(get_database)):
    """Retorna los logs de auditoría ordenados por fecha descendente."""
    cursor = db["historial_cambios_casos"].find().sort("fecha_cambio", -1)
    historial = await cursor.to_list(length=100)
    for h in historial:
        h["_id"] = str(h["_id"])
    return historial


@router.get("/{id_caso}", response_model=CasoResponse)
async def obtener_caso_por_id(id_caso: int, db = Depends(get_database)):
    caso = await db["casos"].find_one({"id_caso": id_caso})
    if not caso:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
    return caso


@router.put("/{id_caso}", response_model=CasoResponse)
async def actualizar_caso(
    id_caso: int, 
    caso_data: CasoUpdate, 
    db = Depends(get_database),
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    # 1. Obtener el estado actual del caso antes de aplicar los cambios
    caso_actual = await db["casos"].find_one({"id_caso": id_caso})
    if not caso_actual:
        raise HTTPException(status_code=404, detail="Caso no encontrado")

    # Filtrar solo los campos enviados por el Frontend que no sean None (excluyendo no especificados)
    campos_a_actualizar = {k: v for k, v in caso_data.model_dump(exclude_unset=True).items() if v is not None}
    
    if not campos_a_actualizar:
        return caso_actual
    
    # ------------------------------------------------------------------
    # BLOQUE 1: PROCESAR HISTORIAL DE CAMBIOS (AUDITORÍA CAMPO POR CAMPO)
    # ------------------------------------------------------------------
    for campo, valor_nuevo in campos_a_actualizar.items():
        valor_anterior = caso_actual.get(campo)
        
        # Si el valor realmente cambió, registramos en el historial
        if valor_anterior != valor_nuevo:
            id_auditoria = await get_next_sequence_value("id_auditoria", db)
            
            registro_auditoria = {
                "id_auditoria": int(id_auditoria),
                "id_caso": int(id_caso),
                "campo_modificado": str(campo),
                "valor_anterior": valor_anterior,
                "valor_nuevo": valor_nuevo,
                "fecha_cambio": datetime.utcnow(),
                "usuario_db": usuario_actual.get("nombre", "Usuario desconocido")
            }
            await db["historial_cambios_casos"].insert_one(registro_auditoria)

    # ------------------------------------------------------------------
    # BLOQUE 2: PROCESAR SEGUIMIENTO (SÓLO SI CAMBIÓ EL ESTADO)
    # ------------------------------------------------------------------
    if "id_estado" in campos_a_actualizar:
        estado_anterior = caso_actual.get("id_estado")
        estado_nuevo = campos_a_actualizar["id_estado"]
        
        if estado_anterior != estado_nuevo:
            id_seguimiento = await get_next_sequence_value("id_seguimiento", db)
            
            registro_seguimiento = {
                "id_seguimiento": int(id_seguimiento),
                "id_caso": int(id_caso),
                "id_usuario_cambio": int(usuario_actual.get("id_usuario", 0)),
                "id_estado_nuevo": int(estado_nuevo),
                "comentarios": campos_a_actualizar.get("descripcion") or f"Cambio de estado a {estado_nuevo}",
                "fecha_actualizacion": datetime.utcnow()
            }
            await db["seguimiento"].insert_one(registro_seguimiento)

    # ------------------------------------------------------------------
    # BLOQUE 3: REALIZAR LA ACTUALIZACIÓN REAL DEL CASO
    # ------------------------------------------------------------------
    caso_actualizado = await db["casos"].find_one_and_update(
        {"id_caso": id_caso},
        {"$set": campos_a_actualizar},
        return_document=True
    )
    
    if not caso_actualizado:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
        
    return caso_actualizado


@router.delete("/{id_caso}", status_code=status.HTTP_200_OK)
async def eliminar_caso(id_caso: int, db = Depends(get_database)):
    # El borrado lógico también altera el campo 'activo', por ende genera auditoría
    caso_actual = await db["casos"].find_one({"id_caso": id_caso})
    if not caso_actual:
        raise HTTPException(status_code=404, detail="Caso no encontrado")
        
    if caso_actual.get("activo") is True:
        id_auditoria = await get_next_sequence_value("id_auditoria", db)
        
        await db["historial_cambios_casos"].insert_one({
            "id_auditoria": int(id_auditoria),
            "id_caso": int(id_caso),
            "campo_modificado": "activo",
            "valor_anterior": True,
            "valor_nuevo": False,
            "fecha_cambio": datetime.utcnow(),
            "usuario_db": "fastapi_backend_user"
        })

    resultado = await db["casos"].find_one_and_update(
        {"id_caso": id_caso},
        {"$set": {"activo": False}},
        return_document=True
    )
    
    return {"message": f"Caso {id_caso} desactivado correctamente y auditado."}
