from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from config import DATABASE_URL
from models.base import Base
from routers import student_routes, attendance_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
  title="Student Attendance Tracker API", 
  version="B-0.1",
)


app.include_router(student_routes.router, prefix="/student", tags=["Students"])
app.include_router(attendance_routes.router, prefix="/attendance", tags=["Attendance"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)