import uuid

from sqlalchemy import UUID
from api.models.sql_alchemy.classgroup_student import ClassGroup_Student
from models.sql_alchemy.classgroup import ClassGroup
from schemas.classgroup import ClassGroupSchema
from services.session_service import session


def create_classgroup(classgroup: ClassGroupSchema, student_ids: list[UUID]):

    new_group = ClassGroup(
        id=uuid.uuid4(),
        name=classgroup.name,
    )

    try:
        session.add(new_group)
        session.flush()

        for student_id in student_ids:
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


