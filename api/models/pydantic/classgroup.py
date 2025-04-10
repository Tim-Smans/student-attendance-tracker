from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from .student import StudentOut


class ClassgroupOut(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)

class ClassgroupWithStudents(BaseModel):
    id: str
    name: str
    students: List[StudentOut]

    model_config = ConfigDict(from_attributes=True)