from datetime import datetime as dt
from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from .attendance import AttendanceOut
from .classgroup import ClassgroupOut

class ClassSessionOut(BaseModel):
    id: UUID  
    classgroup_id: UUID 
    room_device_id: UUID    
    start_time: dt    
    end_time: dt    

    model_config = ConfigDict(from_attributes=True)


from .room_device import RoomDeviceOut
class FullClassSessionOut(BaseModel):
    id: UUID  
    classgroup_id: UUID 
    room_device_id: UUID    
    start_time: dt    
    end_time: dt
    classgroup: ClassgroupOut
    room_device: RoomDeviceOut
    attendances: List[AttendanceOut]


    model_config = ConfigDict(from_attributes=True)