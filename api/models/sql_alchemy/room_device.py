import uuid
from sqlalchemy import UUID, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Import same Base

class RoomDevice(Base):
    __tablename__ = 'RoomDevices'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_name = Column(String, nullable=False)
    device_identifier = Column(String, nullable=False)

    # Foreign Keys & Relations
    class_sessions = relationship("ClassSession", back_populates="room_device", cascade="all, delete")
