from .client import post, get

def check_student_exist(student_id):
    response = get(f"student/{student_id}")
    return response.status_code != 404



def add_student(student_id, institution_id):
    return post("student", {
        "student_id": student_id,
        "institution_id": institution_id
    })
