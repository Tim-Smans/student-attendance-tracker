from uuid import UUID
from models.pydantic.class_session import ClassSessionOut, FullClassSessionOut
from models.sql_alchemy.class_session import ClassSession
from schemas.class_session import ClassSessionSchema
from models.pydantic.paginated_response import PaginatedResponse
from services.session_service import session
from exceptions.not_found_error import NotFoundError
from exceptions.no_id_match_error import NoIdMatchError


def create_session(class_session: ClassSessionSchema):
    new_record = ClassSession(
      classgroup_id=class_session.classgroup_id,
      room_device_id=class_session.room_device_id,
      start_time=class_session.start_time,
      end_time=class_session.end_time
    )   

    try:
        session.add(new_record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def update_session(id: str, new_session: ClassSession):
    og_session = session.query(ClassSession).filter_by(id=id).first()
  
    if UUID(id) != og_session.id:
        raise NoIdMatchError("Session id's do not match", 400)
    
    if not og_session:
        raise NotFoundError("Session does not exist", 404)        

    for key, value in vars(new_session).items():
        if key.startswith('_'):
            continue  # Skip SQLAlchemy internals
        if hasattr(og_session, key):
            setattr(og_session, key, value)
            
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e    

def delete_session(id: str):
    class_session = session.query(ClassSession).filter_by(id=id).first()

    if(class_session):
        session.delete(class_session)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    else:
        raise NotFoundError("Class session does not exist", 404)
        
def get_all_sessions(page: int, limit: int):
    offset = (page - 1) * limit
    total = session.query(ClassSession).offset(offset).limit(limit).count()
    
    class_sessions = session.query(ClassSession).offset(offset).limit(limit).all()

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        items=[ClassSessionOut.model_validate(cs) for cs in class_sessions]  # convert to Pydantic  
        )

def get_full_session(session_id: UUID):

    class_session = session.query(ClassSession).filter_by(id=session_id).first()
    
    print(f"start_time: {class_session.start_time}")
    print(f"endtime: {class_session.end_time}")
    print(f"device: {class_session.room_device_id}")

    return FullClassSessionOut.model_validate(class_session)


def get_attendances_by_session(session_id: str):
    class_sessions = session.query(ClassSession).filter_by(id=session_id).first()

    if(class_sessions):
        return {"attendances": class_sessions.attendances}
    else:
        raise NotFoundError("Class session does not exist", 404)
