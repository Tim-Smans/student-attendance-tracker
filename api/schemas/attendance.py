from pydantic import BaseModel

class AttendanceSchema(BaseModel):
    student_id: str
    room: str

    class Config:
        from_attributes = True