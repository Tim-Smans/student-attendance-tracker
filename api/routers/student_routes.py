import http
from fastapi import Depends
from schemas.student import StudentSchema
from services.student_service import create_student, get_all_students_with_attendance, get_student_with_attendance, update_student, delete_student
from services.auth_service import verify_api_key
from fastapi import APIRouter
from exceptions.not_found_error import NotFoundError
from models.student import Student

router = APIRouter()

@router.get("/", dependencies=[Depends(verify_api_key)])
async def get_students():
    try:
        students = get_all_students_with_attendance()

        return students
    except Exception as e:
        print(e)
        return {"error": str(e)}
    
@router.get("/{id}", dependencies=[Depends(verify_api_key)])
async def get_student_by_id(id: str):
    try:
        student = get_student_with_attendance(id)

        return student
    except Exception as e:
        print(e)
        return {"error": str(e)}
    

@router.delete("/{id}", dependencies=[Depends(verify_api_key)])
async def delete_student_by_id(id: str):
    try:
        delete_student(id)

        return http.HTTPStatus.OK
    except Exception as e:
        print(e)
        return {"error": str(e)}
    
  
@router.post("/", dependencies=[Depends(verify_api_key)])
async def post_student(student: StudentSchema):
    try:
        create_student(student.student_id, student.institution_id)
        return student
    except Exception as e:
        print(e)
        return {"error": str(e)}
    
@router.put("/", dependencies=[Depends(verify_api_key)])
async def put_student(student_id: str, student: StudentSchema):
    try:
        update_student(
            student_id=student_id,
            newStudent=Student(student_id=student.student_id, institution_id=student.institution_id)
        )
        return student
    except Exception as e:
        print(e)
        return {"error": str(e)}    
