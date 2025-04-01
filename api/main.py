from fastapi import FastAPI
from config import DATABASE_URL
from models.sql_alchemy.base import Base
from routers import student_routes, attendance_routes
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
  title="Student Attendance Tracker API", 
  version="B-0.2",
)


app.include_router(student_routes.router, prefix="/student", tags=["Students"])
app.include_router(attendance_routes.router, prefix="/attendance", tags=["Attendance"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
