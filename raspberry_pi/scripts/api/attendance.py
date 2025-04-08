from .client import get, post
from .student import check_student_exist, add_student, is_student_in_session

def add_attendance(student_id, session_id):
    if is_student_in_session(student_id) is False:
        print("Student is not in session")
        return

    return post("attendances", {
        "student_id": student_id,
        "class_session_id": session_id
    })


    