from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class AttendanceOut(BaseModel):
    id: int
    student_id: str
    timestamp: datetime
    room: str

    model_config = ConfigDict(from_attributes=True)