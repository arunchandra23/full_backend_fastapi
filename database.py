from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import logging
import re
DB_URL = "postgresql://postgres:arun@localhost:5432/ott_test"
# DB_URL = "postgresql://postgres:arun@localhost:5432/ott"
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


def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        logging.warning("valid email")
        return True
    else:
        return False