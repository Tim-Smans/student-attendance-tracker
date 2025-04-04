from fastapi import Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from models.sql_alchemy.class_session import ClassSession
from schemas.class_session import ClassSessionSchema
from services.class_session_service import create_session, delete_session, get_all_sessions, get_attendances_by_session, get_full_session, update_session
from services.auth_service import verify_api_key
from fastapi import APIRouter
from exceptions.not_found_error import NotFoundError
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", dependencies=[Depends(verify_api_key)])
async def get_class_sessions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        class_sessions = get_all_sessions(page, limit)

        return class_sessions
    
    except Exception as e:
        logger.error(f"Unexpected error in get_class_sessions: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.get("/{class_session_id}/full", dependencies=[Depends(verify_api_key)])
async def get_session_by_id_full(class_session_id: str):
    try:
        class_session = get_full_session(class_session_id)

        return class_session
    
    except Exception as e:
        logger.error(f"Unexpected error in get_session_by_id_full: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    


@router.delete("/{id}", dependencies=[Depends(verify_api_key)])
async def delete_class_session_by_id(id: str):
    try:
        delete_session(id)

        return JSONResponse(content={"message": "Class session deleted successfully"}, status_code=200)   
         
    except NotFoundError as e:
        raise HTTPException(status_code=e.error_code, detail=f"{e.message}")
    except Exception as e:
        logger.error(f"Unexpected error in delete_room_device_by_id: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
  
@router.post("/", dependencies=[Depends(verify_api_key)], status_code=201)
async def post_class_session(class_session: ClassSessionSchema):
    try:
        create_session(class_session)
        return class_session
    except Exception as e:
        logger.error(f"Unexpected error in post_class_session: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.put("/{class_session_id}", dependencies=[Depends(verify_api_key)])
async def put_class_session(class_session_id: str, new_class_session: ClassSessionSchema):
    try:
        update_session(
            id=class_session_id,
            new_session=new_class_session,
        )   
        return new_class_session
    except Exception as e:
        logger.error(f"Unexpected error in put_class_session: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
