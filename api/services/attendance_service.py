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

    # Add the record to the session and commit it.
    session.add(new_record)
    session.commit()

def get_all_attendances():

    attendances = session.query(Attendance)
    return attendances.all()

def get_attendance_by_id(id: int):
    attendance = session.query(Attendance).filter_by(id=id).first()
    return attendance

def get_attendances_by_date(date: datetime):
    attendances = session.query(Attendance).filter(
        func.date(Attendance.timestamp) == date).all()
    
    return attendances

def delete_attendance(id: int):
    attendance = session.query(Attendance).filter_by(id=id).first()

    if(attendance):
        session.delete(attendance)
        session.commit()
    else:
        raise NotFoundError("Attendance does not exist", 404)