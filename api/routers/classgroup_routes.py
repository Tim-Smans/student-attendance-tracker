from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from ..exceptions.not_found_error import NotFoundError
from ..services.classgroup_service import add_student_to_classgroup, create_classgroup, delete_classgroup, get_classgroup, get_classgroups, get_students_from_classgroup, remove_student_from_classgroup
from ..schemas.classgroup import AddStudentToClassGroupSchema, ClassGroupSchema
from ..services.auth_service import verify_api_key

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", dependencies=[Depends(verify_api_key)], status_code=201)
async def post_classgroup(classgroup: ClassGroupSchema):
    
    try:
        classgroup = create_classgroup(classgroup)
        return classgroup
    except Exception as e:
        logger.error(f"Unexpected error in post_student: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.get("/{classgroup_id}/students", dependencies=[Depends(verify_api_key)])
async def read_students_from_classgroup(
    classgroup_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
    ):
    try:
        students = get_students_from_classgroup(classgroup_id, page, limit)

        return students
    
    except Exception as e:
        logger.error(f"Unexpected error in read_students_from_classgroup: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")


@router.get("/{classgroup_id}/sessions", dependencies=[Depends(verify_api_key)])
async def read_sessions_from_classgroup(classgroup_id: str):
    try:
        students = get_students_from_classgroup(classgroup_id)

        return students
    
    except Exception as e:
        logger.error(f"Unexpected error in read_sessions_from_classgroup: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")


@router.get("/{classgroup_id}", dependencies=[Depends(verify_api_key)])
async def read_classgroup_by_id(
    classgroup_id: str,
    ):
    
    try:
        classgroup = get_classgroup(classgroup_id)

        return classgroup
    
    except Exception as e:
        logger.error(f"Unexpected error in read_classgroup_by_id: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@router.get("/", dependencies=[Depends(verify_api_key)])
async def read_classgroups(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
    ):
    try:
        classgroups = get_classgroups(page, limit)

        return classgroups
    
    except Exception as e:
        logger.error(f"Unexpected error in read_classgroups: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    



@router.delete("/{id}", dependencies=[Depends(verify_api_key)])
async def delete_classgroup_by_id(id: str):
    try:
        delete_classgroup(id)

        return JSONResponse(content={"message": "Classgroup deleted successfully"}, status_code=200)   
         
    except NotFoundError as e:
        raise HTTPException(status_code=e.error_code, detail=f"{e.message}")
    except Exception as e:
        logger.error(f"Unexpected error in delete_student: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.post("/{classgroup_id}/students/{student_id}", dependencies=[Depends(verify_api_key)], status_code=201)
async def post_add_student_to_classgroup(payload: AddStudentToClassGroupSchema):
    try:
        add_student_to_classgroup(payload)

        return JSONResponse(content={"message": "Added student to classgroup"}, status_code=201)   
    except Exception as e:
        logger.error(f"Unexpected error in post_student: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    
@router.delete("/{classgroup_id}/students/{student_id}", dependencies=[Depends(verify_api_key)], status_code=201)
async def delete_student_from_classgroup_route(classgroup_id: str, student_id: str):
    try:
        remove_student_from_classgroup(classgroup_id, student_id)

        return JSONResponse(content={"message": "Removed student from classgroup"}, status_code=200)   
    except Exception as e:
        logger.error(f"Unexpected error in post_student: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")