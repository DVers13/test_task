from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from repository import InMemoryUserRepository, DatabaseUserRepository
from config import settings

DATABASE_URL = settings.db_url
engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(engine)

db_repository = DatabaseUserRepository
memory_repository = InMemoryUserRepository()

def get_db():
    with session_maker() as db:
        yield db

def get_repository(db: Session = Depends(get_db)):
    if settings.repository_type == "memory":
        return memory_repository
    else:
        Base.metadata.create_all(engine)
        return db_repository(db)
