from datetime import datetime
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
