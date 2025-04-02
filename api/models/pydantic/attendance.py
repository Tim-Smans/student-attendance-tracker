from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List

class AttendanceOut(BaseModel):
    id: UUID
    student_id: str
    class_session_id: UUID
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)