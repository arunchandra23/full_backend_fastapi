from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "postgresql://postgres:arun@localhost:5432/ott"
# DB_URL = "sqlite:///./data.db"
engine = create_engine(DB_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autocommit=False,autoflush=False)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        