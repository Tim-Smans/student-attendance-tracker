import datetime
from fastapi import FastAPI
from sqlalchemy import create_engine
from .config import DATABASE_URL
from .models.sql_alchemy.base import Base
from .routers import student_routes, attendance_routes, classgroup_routes, room_device_routes, class_session_routes, status_routes
from .routers.status_routes import last_seen
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
  title="Student Attendance Tracker API", 
  version="B-0.3",
  root_path="/api"
)


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
