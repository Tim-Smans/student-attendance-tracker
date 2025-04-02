from datetime import datetime as dt
from uuid import UUID
from pydantic import BaseModel

class ClassSessionSchema(BaseModel):
    classgroup_id: UUID
    room_device_id: UUID 
    start_time: dt 
    end_time: dt 

    class Config:
        from_attributes = True