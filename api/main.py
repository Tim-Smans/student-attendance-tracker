from fastapi import FastAPI
from sqlalchemy import create_engine
from services.attendance_service import get_all_students, create_student, create_attendance, get_all_students_with_attendance
from schemas.student import StudentSchema
from schemas.attendance import AttendanceSchema
from models.base import Base

app = FastAPI()

@app.get("/students")
async def read_students():
    try:
        students = get_all_students_with_attendance()

        return students
    except Exception as e:
        print(e)
        return {"error": str(e)}
    
  
@app.post("/student")
async def post_student(student: StudentSchema):
    try:
        create_student(student.student_id, student.institution_id)
        return student
    except Exception as e:
        print(e)
        return {"error": str(e)}
    
@app.post("/attendance")
async def post_attendance(attendance: AttendanceSchema):
    try:
        create_attendance(attendance.student_id, attendance.room)
        return attendance
    except Exception as e:
        print(e)
        return {"error": str(e)}