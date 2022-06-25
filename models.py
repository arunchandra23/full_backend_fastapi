from datetime import datetime
from database import Base,engine,SessionLocal
from sqlalchemy import Column, ForeignKey,String,DateTime,Integer,Table,Float
from sqlalchemy.orm import relationship


# junction_movies=Table("movies_watched",Base.metadata,
#                     Column("user_id",Integer,ForeignKey('user.user_id')),
#                     Column("movie_id",Integer,ForeignKey('movie.movie_id'))                      
#                       )

class Watched(Base):
    __tablename__="watched"
    watch_id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('user.user_id'))
    movie_id=Column(Integer,ForeignKey('movie.movie_id'))

class User(Base):
    __tablename__="user"
    user_id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False)
    password =Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    ratings=relationship("Rating",backref="user_rating")
    subscription= relationship("Subscription", backref="user_sub")
    # movies_watched= relationship("Movie",secondary=junction_movies,backref='user_watch')
    
    
class Subscription(Base):
    __tablename__='subscription'
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('user.user_id'))
    start_timestamp = Column(DateTime(timezone=True),default=datetime.utcnow)
    end_timestamp = Column(DateTime(timezone=True),nullable=False)


class Rating(Base):
    __tablename__="rating"
    rating_id=Column(Integer,primary_key=True)
    user_id= Column(Integer,ForeignKey("user.user_id"))
    movie_id=Column(Integer,ForeignKey("movie.movie_id"))
    stars=Column(Float,nullable=False)
    comments=Column(String(3000))
    created_timestamp = Column(DateTime(timezone=True),default=datetime.utcnow,nullable=False)
    # user_id_rel = relationship("User", foreign_keys=[user_id])
    # movies_id_rel = relationship("Movie", foreign_keys=[movie_id])
    # users=relationship("User",back_populates="ratings")
    
        
        
junction_table = Table('movie_genre', Base.metadata,
   Column('movie_id', Integer, ForeignKey('movie.movie_id')),
   Column('genre_id', Integer, ForeignKey('genre.genre_id')),
)


    
class Movie(Base):
    __tablename__="movie"
    movie_id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    description =Column(String(300))      
    language=Column(String(30),nullable=False)
    release_date=Column(DateTime(timezone=True),nullable=False)
    director=Column(String(30),nullable=False)
    ratings=relationship("Rating",backref="movie")
    genres=relationship('Genre',secondary=junction_table,backref="movies")
    
        
        
class Genre(Base):
    __tablename__="genre"
    genre_id=Column(Integer,primary_key=True)
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















