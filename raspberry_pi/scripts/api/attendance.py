from client import post
from student import check_student_exist, add_student

def add_attendance(student_id, room):
    if not check_student_exist(student_id):
        institution_id = student_id.split('.')[0]
        res = add_student(student_id, institution_id)
        if res.status_code != 200:
            return
        

    post("attendance", {
        "student_id": student_id,
        "room": room
    })
