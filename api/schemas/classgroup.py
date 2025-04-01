from pydantic import BaseModel

from api.schemas.student import StudentSchema

class ClassGroupSchema(BaseModel):
    name: str
    students: list[StudentSchema]

    class Config: 
        from_attributes = True