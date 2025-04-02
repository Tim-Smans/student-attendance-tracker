from pydantic import BaseModel

class ClassGroupSchema(BaseModel):
    name: str
    student_ids: list[str]

    class Config: 
        from_attributes = True

class AddStudentToClassGroupSchema(BaseModel):
    classgroup_id: str
    student_id: str

    class Config: 
        from_attributes = True