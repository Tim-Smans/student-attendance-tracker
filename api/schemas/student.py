from pydantic import BaseModel

class StudentSchema(BaseModel):
    student_id: str
    lastname = str 
    firstname = str  
    email = str 
    degree_programme = str  

    class Config:
        from_attributes = True