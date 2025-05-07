import datetime
from fastapi import FastAPI
from sqlalchemy import create_engine
from .config import DATABASE_URL
from .models.sql_alchemy.base import Base
from .routers import student_routes, attendance_routes, classgroup_routes, room_device_routes, class_session_routes, status_routes
from .routers.status_routes import last_seen
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(
  title="Student Attendance Tracker API", 
  version="B-0.3",
)


# Metrics setup
device_up = Gauge("device_up", "Device online status", ['device_id'])


@app.get("/metrics")
def metrics():
    # Update device_up metric vóór het exporteren
    now = datetime.now()
    for device_id, last in last_seen.items():
        is_up = (now - last) < timedelta(minutes=2)
        device_up.labels(device_id=device_id).set(1 if is_up else 0)

    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}



app.include_router(student_routes.router, prefix="/students", tags=["Students"])
app.include_router(attendance_routes.router, prefix="/attendances", tags=["Attendances"])
app.include_router(classgroup_routes.router, prefix="/classgroups", tags=["Classgroups"])
app.include_router(room_device_routes.router, prefix="/roomdevices", tags=["Room Devices"])
app.include_router(class_session_routes.router, prefix="/classsessions", tags=["Class Sessions"])
app.include_router(status_routes.router, prefix="/status", tags=["Status"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
