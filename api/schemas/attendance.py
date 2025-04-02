from pydantic import BaseModel

class AttendanceSchema(BaseModel):
    student_id: str
    class_session_id: str

    class Config:
        from_attributes = True