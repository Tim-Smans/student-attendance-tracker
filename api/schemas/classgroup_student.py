from pydantic import BaseModel

class ClassGroup_StudentSchema(BaseModel):
    id: str
    classgroup_id: str
    student_id: str

    class Config:
        from_attributes = True