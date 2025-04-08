from .client import post, get
from .session import get_active_session

def check_student_exist(student_id):
    response = get(f"student/{student_id}")
    return response.status_code != 404



def add_student(student_id, institution_id):
    return post("student", {
        "student_id": student_id,
        "institution_id": institution_id
    })

def get_students_from_session():
    """
    Gets the students in the current session, if any.

    Returns:
        list: A list of students in the current session, or an empty list if no session is active.
    """
    session = get_active_session()

    if session is None:
        return []

    if(session['classgroup_id'] is None):
        return []

    students = get(f"classgroups/{session['classgroup_id']}/students")

    return students

def is_student_in_session(student_id):
    """
    Checks if a student is in the current session.

    Args:
        student_id (str): The id of the student to check.

    Returns:
        bool: True if the student is in the current session, False otherwise.
    """
    session = get_active_session()

    if session is None:
        return False

    if(session['classgroup_id'] is None):
        return False

    students = get(f"classgroups/{session['classgroup_id']}/students")

    for student in students.json():
        if student['student_id'] == student_id:
            return True

    return False
