from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from models.pydantic.attendance import AttendanceOut


class StudentWithAttendanceOut(BaseModel):
    student_id: str
    lastname = str 
    firstname = str  
    email = str 
    degree_programme = str  

    attendances: List[AttendanceOut]

    model_config = ConfigDict(from_attributes=True)

class StudentOut(BaseModel):
    student_id: str
    lastname = str 
    firstname = str  
    email = str 
    degree_programme = str  
    
    model_config = ConfigDict(from_attributes=True)