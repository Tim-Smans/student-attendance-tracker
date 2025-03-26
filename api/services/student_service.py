from models.student import Student
from services.session_service import session



def create_student(student_id: str, institution_id: str):
    new_record = Student(
    student_id=student_id,
    institution_id=institution_id
    )   

    # Add the record to the session and commit it.
    session.add(new_record)
    session.commit()


def get_all_students():
    students = session.query(Student)
    return students.all()

def get_all_students_with_attendance():
    students = session.query(Student)
    return { student.student_id: student.attendances for student in students }

def delete_student(student_id: str):
    student = session.query(Student).filter_by(student_id=student_id).first()

    if(student):
        session.delete(student)
        session.commit
        print("Deleted student")
    else:
        print("Student does not exist")