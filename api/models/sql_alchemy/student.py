from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base  # Import the shared Base

class Student(Base):
    __tablename__ = 'Students'

    student_id = Column(String, primary_key=True)
    lastname = Column(String, nullable=True)    
    firstname = Column(String, nullable=True)    
    email = Column(String, nullable=True)    
    degree_programme = Column(String, nullable=True)    

    # Foreign Keys & Relations
    attendances = relationship("Attendance", back_populates="student", cascade="all, delete")
    classgroup_students = relationship("ClassGroup_Student", back_populates="student", cascade="all, delete")
