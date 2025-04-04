from fastapi import Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from models.pydantic.room_device import RoomDeviceWithSessionsOut
from models.sql_alchemy.room_device import RoomDevice
from schemas.room_device import RoomDeviceSchema
from services.room_device_service import create_device, delete_device, get_all_devices, get_class_sessions_from_device, update_device
from services.auth_service import verify_api_key
from fastapi import APIRouter
from exceptions.not_found_error import NotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", dependencies=[Depends(verify_api_key)])
async def get_room_devices(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        room_devices = get_all_devices(page, limit)

        return room_devices
    
    except Exception as e:
        logger.error(f"Unexpected error in get_room_devices: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.get("/{device_id}/sessions", dependencies=[Depends(verify_api_key)], response_model=RoomDeviceWithSessionsOut)
async def get_sessions_from_device_by_id(device_id: str):
    try:
        room_device = get_class_sessions_from_device(device_id)

        return RoomDeviceWithSessionsOut.model_validate(room_device)
        
    except Exception as e:
        logger.error(f"Unexpected error in get_sessions_from_device_by_id: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    


@router.delete("/{id}", dependencies=[Depends(verify_api_key)])
async def delete_room_device_by_id(id: str):
    try:
        delete_device(id)

        return JSONResponse(content={"message": "Room device deleted successfully"}, status_code=200)   
         
    except NotFoundError as e:
        raise HTTPException(status_code=e.error_code, detail=f"{e.message}")
    except Exception as e:
        logger.error(f"Unexpected error in delete_room_device_by_id: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
  
@router.post("/", dependencies=[Depends(verify_api_key)], status_code=201)
async def post_device(room_device: RoomDeviceSchema):
    try:
        create_device(room_device)
        return room_device
    except Exception as e:
        logger.error(f"Unexpected error in post_device: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.put("/{room_device_id}", dependencies=[Depends(verify_api_key)])
async def put_room_device(room_device_id: str, new_room_device: RoomDeviceSchema):
    try:
        update_device(
            id=room_device_id,
            new_room_device=RoomDevice(
                room_name=new_room_device.room_name,
                device_identifier=new_room_device.device_identifier
            )
        )
        return new_room_device
    except Exception as e:
        logger.error(f"Unexpected error in put_room_device: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
