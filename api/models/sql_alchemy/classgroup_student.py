import uuid
from sqlalchemy import UUID, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Import same Base

class ClassGroup_Student(Base):
    __tablename__ = 'ClassGroup_Student'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign Keys & Relations
    classgroup_id = Column(
        UUID, 
        ForeignKey('ClassGroups.id'), 
        nullable=False, 
        )
    student_id = Column(
        String, 
        ForeignKey('Students.student_id'), 
        nullable=False, 
        )
    
    classgroup = relationship("ClassGroup", back_populates="classgroup_students")
    student = relationship("Student", back_populates="classgroup_students")

