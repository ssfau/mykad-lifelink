
import os
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, ForeignKey, JSON, Boolean, Date
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Mapped, mapped_column
from typing import List, Dict
from datetime import date

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = "sqlite:///" + os.path.join(basedir, 'app.db')

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


