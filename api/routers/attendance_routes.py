from fastapi import Depends
from schemas.attendance import AttendanceSchema
from services.attendance_service import create_attendance
from services.auth_service import verify_api_key
from fastapi import APIRouter

router = APIRouter()

@router.post("/", dependencies=[Depends(verify_api_key)])
async def post_attendance(attendance: AttendanceSchema):
    try:
        create_attendance(attendance.student_id, attendance.room)
        return attendance
    except Exception as e:
        print(e)
        return {"error": str(e)}
    
