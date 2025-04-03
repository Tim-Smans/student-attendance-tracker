import uuid
from models.pydantic.classgroup import ClassgroupOut
from models.sql_alchemy.student import Student
from exceptions.not_found_error import NotFoundError
from schemas.student import StudentSchema
from models.pydantic.paginated_response import PaginatedResponse
from models.sql_alchemy.classgroup_student import ClassGroup_Student
from models.sql_alchemy.classgroup import ClassGroup
from schemas.classgroup import AddStudentToClassGroupSchema, ClassGroupSchema
from services.session_service import session


def create_classgroup(classgroup: ClassGroupSchema):

    new_group = ClassGroup(
        id=uuid.uuid4(),
        name=classgroup.name,
    )

    try:
        session.add(new_group)
        session.flush()

        for student_id in classgroup.student_ids:
            link = ClassGroup_Student(
                id=uuid.uuid4(),
                classgroup_id=new_group.id,
                student_id=student_id
            )
            session.add(link)

        session.commit()
        return new_group

    except Exception as e:
        session.rollback()
        raise e


def get_students_from_classgroup(classgroup_id: str, page: int, limit: int):
    offset = (page - 1) * limit
    total = session.query(ClassGroup_Student).filter_by(classgroup_id=classgroup_id).count()

    links = session.query(ClassGroup_Student).filter_by(classgroup_id=classgroup_id).offset(offset).limit(limit).all()
    students = [link.student for link in links]

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=[StudentSchema.model_validate(s) for s in students]  # convert to Pydantic  
        )

def get_classgroups(page: int, limit: int):
    offset = (page - 1) * limit
    total = session.query(ClassGroup).count()

    classgroups = session.query(ClassGroup).offset(offset).limit(limit).all()

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=[ClassgroupOut.model_validate(cg) for cg in classgroups]  # convert to Pydantic  
        )


def get_classgroup(classgroup_id: str):
    classgroup = session.query(ClassGroup).filter_by(id=classgroup_id).first()

    if(classgroup):
        return classgroup
    else:
        raise NotFoundError("Classgroup does not exist", 404)

def delete_classgroup(classgroup_id: str):
    classgroup = session.query(ClassGroup).filter_by(id=classgroup_id).first()

    if(classgroup):
        session.delete(classgroup)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    else:
        raise NotFoundError("Classgroup does not exist", 404)
    

def add_student_to_classgroup(payload: AddStudentToClassGroupSchema):
    classgroup = session.query(ClassGroup).filter_by(id=payload.classgroup_id).first()
    student = session.query(Student).filter_by(student_id=payload.student_id).first()

    if not student:
        raise NotFoundError("Student does not exist", 404)

    if classgroup:
        link = ClassGroup_Student(
            id=uuid.uuid4(),
            classgroup_id=classgroup.id,
            student_id=payload.student_id
        )
        session.add(link)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    else:
        raise NotFoundError("Classgroup does not exist", 404)
    
def remove_student_from_classgroup(classgroup_id: str, student_id: str):
    classgroup = session.query(ClassGroup).filter_by(id=classgroup_id).first()
    student = session.query(Student).filter_by(student_id=student_id).first()

    if not student:
        raise NotFoundError("Student does not exist", 404)

    if classgroup:
        link = session.query(ClassGroup_Student).filter_by(classgroup_id=classgroup.id, student_id=student_id).first()
        session.delete(link)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    else:
        raise NotFoundError("Classgroup does not exist", 404)