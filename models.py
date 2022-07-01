from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
import uuid
from traitlets import default
from database import Base,engine,SessionLocal
from sqlalchemy import Column, ForeignKey,String,DateTime,Integer,Table,Float
from sqlalchemy.orm import relationship


class Watched(Base):
    __tablename__="watched"
    watch_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),ForeignKey('user.user_id'))
    movie_id=Column(UUID(as_uuid=True),ForeignKey('movie.movie_id'))

class User(Base):
    __tablename__="user"
    user_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False)
    password =Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    ratings=relationship("Rating",backref="user_rating")
    subscription= relationship("Subscription", backref="user_sub")
    
    
class Subscription(Base):
    __tablename__='subscription'
    id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    user_id=Column(UUID(as_uuid=True),ForeignKey('user.user_id'))
    start_timestamp = Column(DateTime(timezone=True),default=datetime.utcnow)
    end_timestamp = Column(DateTime(timezone=True),nullable=False)


class Rating(Base):
    __tablename__="rating"
    rating_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    user_id= Column(UUID(as_uuid=True),ForeignKey("user.user_id"))
    movie_id=Column(UUID(as_uuid=True),ForeignKey("movie.movie_id"))
    stars=Column(Float,nullable=False)
    comments=Column(String(3000))
    created_timestamp = Column(DateTime(timezone=True),default=datetime.utcnow,nullable=False)
        
        
junction_table = Table('movie_genre', Base.metadata,
   Column('movie_id', UUID(as_uuid=True), ForeignKey('movie.movie_id')),
   Column('genre_id', UUID(as_uuid=True), ForeignKey('genre.genre_id')),
)


    
class Movie(Base):
    __tablename__="movie"
    movie_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    title=Column(String,nullable=False)
    description =Column(String(300))      
    language=Column(String(30),nullable=False)
    release_date=Column(DateTime(timezone=True),nullable=False)
    director=Column(String(30),nullable=False)
    ratings=relationship("Rating",backref="movie")
    genres=relationship('Genre',secondary=junction_table,backref="movies")
    
        
        
class Genre(Base):
    __tablename__="genre"
    genre_id=Column(UUID(as_uuid=True),default=uuid.uuid4,primary_key=True)
    genre_name=Column(String(50),nullable=False)
    
    



















# class Action(Base):
#     __tablename__="action"
#     id = Column(Integer,primary_key=True)
#     movie_name=Column(String,nullable=False)
#     genre=Column(String,nullable=False)
#     description =Column(String,nullable=False)
    
#     class Config:
#         orm_mode=True
        
# class Romance(Base):
#     __tablename__="romance"
#     id = Column(Integer,primary_key=True)
#     movie_name=Column(String,nullable=False)
#     genre=Column(String,nullable=False)
#     description =Column(String,nullable=False)
    
#     class Config:
#         orm_mode=True

# class Comedy(Base):
#     __tablename__="comedy"
#     id = Column(Integer,primary_key=True)
#     movie_name=Column(String,nullable=False)
#     genre=Column(String,nullable=False)
#     description =Column(String,nullable=False)
    
#     class Config:
#         orm_mode=True
        
# class Thriller(Base):
#     __tablename__="thriller"
#     id = Column(Integer,primary_key=True)
#     movie_name=Column(String,nullable=False)
#     genre=Column(String,nullable=False)
#     description =Column(String,nullable=False)
    
#     class Config:
#         orm_mode=True
    


# data = User(name='arun',email='arun@email.com',password="123")
# db=SessionLocal()
# db.add(data)
# db.commit()
# db.refresh(data)















