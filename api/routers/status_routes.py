
from datetime import datetime, timedelta
import logging
from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ..schemas.ping import PingSchema

from ..services.auth_service import verify_api_key


logger = logging.getLogger(__name__)
router = APIRouter()
last_seen: Dict[str, datetime] = {}

@router.post("/ping", dependencies=[Depends(verify_api_key)])
async def ping(payload: PingSchema):
    last_seen[payload.id] = datetime.now()
    return JSONResponse(content={"message": "pong"})


@router.get("/is_online/{pi_id}", dependencies=[Depends(verify_api_key)])
async def is_online(pi_id: str):
    last = last_seen.get(pi_id)
    if not last:
        return {"online": False}
    online = datetime.now() - last < timedelta(minutes=2)
    return JSONResponse(content={"online": online})
