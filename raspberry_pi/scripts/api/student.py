from api.client import post, get
from raspberry_pi.scripts.api.session import get_active_session

def check_student_exist(student_id):
    response = get(f"student/{student_id}")
    return response.status_code != 404



def add_student(student_id, institution_id):
    return post("student", {
        "student_id": student_id,
        "institution_id": institution_id
    })

def get_students_from_session(session_id):
    session = get_active_session()

    if session is None:
        return []

    return session["students"]
