from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "postgresql+pg8000://postgres:postgresPassword@localhost:5432/postgres"
)


Session = sessionmaker(bind=engine)
session = Session()