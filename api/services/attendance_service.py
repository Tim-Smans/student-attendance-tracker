from datetime import datetime

from sqlalchemy import func
from exceptions.not_found_error import NotFoundError
from services.session_service import session
from models.base import Base
from models.student import Student
from models.attendance import Attendance


def create_attendance(student_id: str, room: str):
    new_record = Attendance(
    student_id=student_id,
    timestamp=datetime.now(),
    room=room
    )   

    session.add(new_record)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def get_all_attendances():
    attendances = session.query(Attendance)
    return attendances.all()

def get_attendance_by_id(id: int):
    attendance = session.query(Attendance).filter_by(id=id).first()

    if not attendance:
        raise NotFoundError("Attendance does not exist", 404)

    return attendance

def get_attendances_by_date(date: datetime):
    attendances = session.query(Attendance).filter(
        func.date(Attendance.timestamp) == date).all()
    
    return attendances

def delete_attendance(id: int):
    attendance = get_attendance_by_id(id)
        
    session.delete(attendance)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    