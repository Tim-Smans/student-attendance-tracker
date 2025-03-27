from models.student import Student
from services.session_service import session
from exceptions.not_found_error import NotFoundError
from exceptions.no_id_match_error import NoIdMatchError


def create_student(student_id: str, institution_id: str):
    new_record = Student(
    student_id=student_id,
    institution_id=institution_id
    )   

    try:
        session.add(new_record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def update_student(student_id: str, newStudent: Student):
    og_student = session.query(Student).filter_by(student_id=student_id).first()
    
    if student_id != newStudent.student_id:
        raise NoIdMatchError("Student id's do not match", 400)
    
    if og_student:
        for key, value in vars(newStudent).items():
            if key.startswith('_'):
                continue  # Skip SQLAlchemy internals
            if hasattr(og_student, key):
                setattr(og_student, key, value)
                
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e    
    else:
        raise NotFoundError("Student does not exist", 404)        

def delete_student(student_id: str):
    student = session.query(Student).filter_by(student_id=student_id).first()

    if(student):
        session.delete(student)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    else:
        raise NotFoundError("Student does not exist", 404)
        
def get_all_students():
    students = session.query(Student)
    return students.all()

def get_all_students_with_attendance():
    students = session.query(Student)
    return { student.student_id: student.attendances for student in students }

def get_student_with_attendance(student_id: str):
    student = session.query(Student).filter_by(student_id=student_id).first()
    
    if not student:
        raise NotFoundError("Student does not exist", 404)
    
    return { student.student_id: student.attendances}
