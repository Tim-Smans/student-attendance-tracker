from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict



class RoomDeviceOut(BaseModel):
    id: UUID  
    room_name: str 
    device_identifier: str    

    model_config = ConfigDict(from_attributes=True)


from models.pydantic.class_session import ClassSessionOut
class RoomDeviceWithSessionsOut(BaseModel):
    id: UUID  
    room_name: str 
    device_identifier: str
    class_sessions: List[ClassSessionOut]    

    model_config = ConfigDict(from_attributes=True)

