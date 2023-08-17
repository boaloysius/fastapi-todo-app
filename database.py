import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = os.getenv("DB_URL")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SQLALCHEMY_DB_URL = DB_URL.format(password=DB_PASSWORD)
engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
