from datetime import datetime

from sqlalchemy import func
from ..models.pydantic.paginated_response import PaginatedResponse
from ..models.pydantic.attendance import AttendanceOut
from ..exceptions.not_found_error import NotFoundError
from ..services.session_service import session
from ..models.sql_alchemy.base import Base
from ..models.sql_alchemy.student import Student
from ..models.sql_alchemy.attendance import Attendance


def create_attendance(student_id: str, class_session_id: str):
    new_record = Attendance(
    student_id=student_id,
    timestamp=datetime.now(),
    class_session_id=class_session_id
    )   

    session.add(new_record)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def get_all_attendances(page: int, limit: int):
    offset = (page - 1) * limit
    total = session.query(Attendance).count()
    attendances = session.query(Attendance).offset(offset).limit(limit).all()

    pydantic_attendances = [
        AttendanceOut(
            id=a.id,
            student_id=a.student_id,
            timestamp=a.timestamp,
            class_session_id=a.class_session_id
        )    
        for a in attendances
    ]

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=pydantic_attendances
    )

def get_attendance_by_id(id: int):
    attendance = session.query(Attendance).filter_by(id=id).first()

    if not attendance:
        raise NotFoundError("Attendance does not exist", 404)

    return attendance

def get_attendances_by_date(date: datetime, page: int, limit: int):
    offset = (page - 1) * limit
    total = session.query(Attendance).count()
    attendances = session.query(Attendance).filter(
        func.date(Attendance.timestamp) == date).offset(offset).limit(limit).all()
    
    pydantic_attendances = [
        AttendanceOut(
            id=a.id,
            student_id=a.student_id,
            timestamp=a.timestamp,
            class_session_id=a.class_session_id
        )    
        for a in attendances
    ]

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=pydantic_attendances
    )

def delete_attendance(id: int):
    attendance = get_attendance_by_id(id)
        
    session.delete(attendance)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    