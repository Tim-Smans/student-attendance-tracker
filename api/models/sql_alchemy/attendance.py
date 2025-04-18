import uuid
from sqlalchemy import UUID, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Import same Base

class Attendance(Base):
    __tablename__ = 'Attendances'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, nullable=False)
    
    # Foreign Keys & Relations
    student_id = Column(
        String, 
        ForeignKey('Students.student_id'), 
        nullable=False, 
        )
    class_session_id = Column(
        UUID, 
        ForeignKey('ClassSessions.id'), 
        nullable=False, 
        )

    student = relationship("Student", back_populates="attendances")
    class_session = relationship("ClassSession", back_populates="attendances")
