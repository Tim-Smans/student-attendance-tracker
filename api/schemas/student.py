from pydantic import BaseModel

class StudentSchema(BaseModel):
    student_id: str
    institution_id: str

    class Config:
        from_attributes = True