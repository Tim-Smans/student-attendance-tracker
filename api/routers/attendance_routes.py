from datetime import datetime
from fastapi import Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from sqlalchemy import Date
from exceptions.not_found_error import NotFoundError
from schemas.attendance import AttendanceSchema
from services.attendance_service import create_attendance, delete_attendance, get_all_attendances, get_attendance_by_id, get_attendances_by_date
from services.auth_service import verify_api_key
from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", dependencies=[Depends(verify_api_key)], status_code=201)
async def post_attendance(attendance: AttendanceSchema):
    try:
        create_attendance(attendance.student_id, attendance.room)
        return attendance
    except Exception as e:
        logger.error(f"Unexpected error in post_attendance: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    

@router.delete("/{id}", dependencies=[Depends(verify_api_key)])
async def delete_attendance_by_id(id: int):
    try:
        delete_attendance(id)

        return JSONResponse(content={"message": "Attendance deleted successfully"}, status_code=200)   
         
    except NotFoundError as e:
        raise HTTPException(status_code=e.error_code, detail=f"{e.message}")
    except Exception as e:
        logger.error(f"Unexpected error in delete_attendance_by_id: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.get("/", dependencies=[Depends(verify_api_key)])
async def get_attendances_all():
    try:
        attendances = get_all_attendances()
        return attendances
    except Exception as e:
        logger.error(f"Unexpected error in get_attendances_all: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.get("/{id}", dependencies=[Depends(verify_api_key)])
async def get_attendances_by_id(id: int):
    try:
        attendance = get_attendance_by_id(id)
        return attendance
    except Exception as e:
        logger.error(f"Unexpected error in get_attendances_by_id: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@router.get("/date/{yyy-mm-dd}", dependencies=[Depends(verify_api_key)])
async def get_attendances_by_date_route(date: str):    
    
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()

        attendances = get_attendances_by_date(parsed_date)
        return attendances
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date, use 'YYYY-MM-DD'")
    except Exception as e:
        logger.error(f"Unexpected error in get_attendances_by_date_route: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    