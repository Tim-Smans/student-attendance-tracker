import uuid
from sqlalchemy import UUID, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Import same Base

class ClassSession(Base):
    __tablename__ = 'ClassSessions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    # Foreign Keys & Relations
    classgroup_id = Column(
        UUID, 
        ForeignKey('ClassGroups.id'), 
        nullable=False, 
        )

    room_device_id = Column(
        UUID, 
        ForeignKey('RoomDevices.id'), 
        nullable=False, 
        )

    classgroup = relationship("ClassGroup", back_populates="class_sessions")
    room_device = relationship("RoomDevice", back_populates="class_sessions")
    attendances = relationship("Attendance", back_populates="class_session", cascade="all, delete")
