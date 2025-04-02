from datetime import datetime as dt
from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ClassSessionOut(BaseModel):
    id: UUID  
    classgroup_id: UUID 
    room_device_id: UUID    
    start_time: dt    
    end_time: dt    

    model_config = ConfigDict(from_attributes=True)