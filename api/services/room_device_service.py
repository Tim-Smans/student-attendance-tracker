from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo
from fastapi import HTTPException
from models.sql_alchemy.class_session import ClassSession
from models.pydantic.room_device import RoomDeviceOut
from models.sql_alchemy.room_device import RoomDevice
from schemas.room_device import RoomDeviceSchema
from models.pydantic.paginated_response import PaginatedResponse
from services.session_service import session
from exceptions.not_found_error import NotFoundError
from exceptions.no_id_match_error import NoIdMatchError


def create_device(room_device: RoomDeviceSchema):
    new_record = RoomDevice(
      room_name=room_device.room_name,
      device_identifier=room_device.device_identifier
    )   

    try:
        session.add(new_record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def update_device(id: str, new_room_device: RoomDevice):
    og_room_device = session.query(RoomDevice).filter_by(id=id).first()
  
    if UUID(id) != og_room_device.id:
        raise NoIdMatchError("Room Device id's do not match", 400)
    
    if not og_room_device:
        raise NotFoundError("Room device does not exist", 404)        

    for key, value in vars(new_room_device).items():
        if key.startswith('_'):
            continue  # Skip SQLAlchemy internals
        if hasattr(og_room_device, key):
            setattr(og_room_device, key, value)
            
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e    

def delete_device(id: str):
    room_device = session.query(RoomDevice).filter_by(id=id).first()

    if(room_device):
        session.delete(room_device)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    else:
        raise NotFoundError("Room device does not exist", 404)
        
def get_all_devices(page: int, limit: int):
    offset = (page - 1) * limit
    total = session.query(RoomDevice).offset(offset).limit(limit).count()
    
    room_devices = session.query(RoomDevice).offset(offset).limit(limit).all()

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=[RoomDeviceOut.model_validate(rd) for rd in room_devices]  # convert to Pydantic  
        )

def get_class_sessions_from_device(device_id: str):
    room_device = session.query(RoomDevice).filter(RoomDevice.id == device_id).first()

    if not room_device:
        raise NotFoundError("Room device does not exist", 404)

    return room_device

from datetime import datetime
from zoneinfo import ZoneInfo

def get_active_session_from_device(device_id: str):
    now = datetime.now(ZoneInfo("Europe/Helsinki"))

    print(f"time: {now}")
    print(f"device_id: {device_id}")

    active_session = (
        session.query(ClassSession)
        .filter(ClassSession.room_device_id == device_id)
        .first()
    )

    if not active_session:
        raise NotFoundError("No active session found.", 404)

    start_time = active_session.start_time
    end_time = active_session.end_time

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=ZoneInfo("Europe/Helsinki"))
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=ZoneInfo("Europe/Helsinki"))

    if start_time <= now <= end_time:
        return active_session
    else:
        raise NotFoundError("No active session found.", 404)


def get_device_by_identifier(device_identifier: str):
    
    
    room_device = (
        session.query(RoomDevice)
        .filter(RoomDevice.device_identifier == device_identifier)
        .first()
    )

    if not room_device:
        raise NotFoundError("No room device found with that identigier.", 404)

    return room_device