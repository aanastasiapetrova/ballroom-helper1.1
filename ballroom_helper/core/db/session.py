from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql://postgres:postgres@localhost/helper"
engine = create_engine(DATABASE_URL, echo=True)
session_maker = sessionmaker(bind=engine, future=True)


def get_session():
    with session_maker() as session:
        yield session