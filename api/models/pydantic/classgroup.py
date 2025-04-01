from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from models.pydantic.student import StudentOut


class Classgroup(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)

class ClassgroupWithStudents(BaseModel):
    id: str
    name: str
    students: List[StudentOut]

    model_config = ConfigDict(from_attributes=True)