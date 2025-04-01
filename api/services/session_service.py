from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.sql_alchemy.base import Base
from config import DATABASE_URL


engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()