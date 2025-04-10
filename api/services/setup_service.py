from ..models.sql_alchemy.base import Base
from ..models.sql_alchemy.classgroup import ClassGroup  # 🔥 nodig!
from ..models.sql_alchemy.classgroup_student import ClassGroup_Student
from ..models.sql_alchemy.class_session import ClassSession
from ..models.sql_alchemy.student import Student
from ..models.sql_alchemy.attendance import Attendance
from ..models.sql_alchemy.room_device import RoomDevice

_ = [ClassGroup, ClassGroup_Student, ClassSession, Student, Attendance, RoomDevice]

from sqlalchemy import create_engine
from config import DATABASE_URL

def setup_database():                                                 
  engine = create_engine(DATABASE_URL)
  Base.metadata.create_all(engine)