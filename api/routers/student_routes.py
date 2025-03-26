from fastapi import Depends
from schemas.student import StudentSchema
from services.student_service import create_student, get_all_students_with_attendance
from services.auth_service import verify_api_key
from fastapi import APIRouter

router = APIRouter()

@router.get("/", dependencies=[Depends(verify_api_key)])
async def get_students():
    try:
        students = get_all_students_with_attendance()

        return students
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