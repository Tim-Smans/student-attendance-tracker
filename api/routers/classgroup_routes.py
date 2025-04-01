from fastapi import APIRouter, Depends, HTTPException
from services.classgroup_service import create_classgroup
from schemas.classgroup import ClassGroupSchema
from schemas.student import StudentSchema
from services.auth_service import verify_api_key

import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", dependencies=[Depends(verify_api_key)], status_code=201)
async def post_classgroup(classgroup: ClassGroupSchema):
    try:
        create_classgroup(classgroup)
        return student
    except Exception as e:
        logger.error(f"Unexpected error in post_student: {e}")   
        raise HTTPException(status_code=500, detail=f"{str(e)}")