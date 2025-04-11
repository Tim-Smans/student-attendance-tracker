from ..schemas.student import StudentSchema
from ..models.pydantic.attendance import AttendanceOut
from ..models.pydantic.student import StudentWithAttendanceOut
from ..models.pydantic.paginated_response import PaginatedResponse
from ..models.sql_alchemy.student import Student
from ..services.session_service import session
from ..exceptions.not_found_error import NotFoundError
from ..exceptions.no_id_match_error import NoIdMatchError


def create_student(student: StudentSchema):
    new_record = Student(
    student_id=student.student_id,
    lastname=student.lastname,
    firstname=student.firstname,
    email=student.email,
    degree_programme=student.degree_programme,
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


def get_all_students_with_attendance(page: int, limit: int):
    offset = (page - 1) * limit
    total = session.query(Student).count()
    students = session.query(Student).offset(offset).limit(limit).all()

    pydantic_students = [
        StudentWithAttendanceOut(
            student_id=s.student_id,
            lastname=s.lastname,
            firstname=s.firstname,
            email=s.email,
            degree_programme=s.degree_programme,
            attendances=[
                AttendanceOut(
                    id=a.id,
                    student_id=a.student_id,
                    timestamp=a.timestamp,
                    room=a.room
                )
                for a in s.attendances
            ]
        )
        for s in students
    ]
    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=pydantic_students
    )

def get_student_with_attendance(student_id: str):
    student = session.query(Student).filter_by(student_id=student_id).first()
    
    if not student:
        raise NotFoundError("Student does not exist", 404)
    


    return { student }
