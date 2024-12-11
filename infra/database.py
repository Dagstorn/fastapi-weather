import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL_ENV = os.getenv("DATABASE_URL")
print("DATABASE_URL_ENV")
print(DATABASE_URL_ENV)
if not DATABASE_URL_ENV:
    DATABASE_URL = "sqlite:///./weather.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL_ENV)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()