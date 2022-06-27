from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "postgresql://bfrxegdlyokgoz:e7f5c214a58219673eec9b577c2e6288e659801817e55592d3a44f27be4ab422@ec2-3-222-74-92.compute-1.amazonaws.com:5432/d55vkls8p7vq7l"
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
        