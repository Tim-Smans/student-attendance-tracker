from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from models.pydantic.attendance import AttendanceOut


class StudentWithAttendanceOut(BaseModel):
    student_id: str
    attendances: List[AttendanceOut]

    model_config = ConfigDict(from_attributes=True)