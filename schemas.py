from datetime import datetime
from turtle import title
from pydantic import BaseModel, Field
from typing import List,Union
from uuid import uuid4, UUID

class User_schema(BaseModel):
    name:str
    email:str
    password:str
    subscription_expires:datetime
    class Config:
        orm_mode=True
        
class Subscription(BaseModel):
    user_id:UUID = Field(default_factory=uuid4)
    start_timestamp : datetime
    end_timestamp:datetime
    
    class Config:
        orm_mode=True

class Review_schema(BaseModel):
    #Get the user-id of logged in user from the FastApi and add it to the table using add()
    title:str
    stars:float
    comments:str
    
    class Config:
        orm_mode=True


class Genre_schema(BaseModel):
    genre_name:str
    
    class Config:
        orm_mode=True


class Movie_schema(BaseModel):
    title:str
    description:str
    language:str
    release_date:datetime
    director:str
    genres:list[str]
    
    
    class Config:
        orm_mode=True
        
        

class User_response_schema(BaseModel):
    user_id:UUID = Field(default_factory=uuid4)    
    name:str
    email:str
    created_at:datetime
    # ratings:List[Review_schema]
    subscription:List[Subscription]
    class Config:
        orm_mode=True  
        
        
class Movie_response_schema(BaseModel):
    movie_id:UUID = Field(default_factory=uuid4)
    title:str
    description:str
    language:str
    release_date:datetime
    director:str
    genres:List[Genre_schema]
    ratings:list[Review_schema]
    
    class Config:
        orm_mode=True



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

        
# Schemas for getting custom inputs

class Watch(BaseModel):
    title:str
    
    class Config:
        orm_mode=True
        
class Login(BaseModel):
    username:str
    password:str
    
    class Config:
        orm_mode=True
        
        
class Rating(BaseModel):
    created_timestamp:datetime
    rating_id:UUID = Field(default_factory=uuid4)
    user_id:UUID = Field(default_factory=uuid4)    
    stars:float
    comments:str
    class Config:
        orm_mode=True


class GMovie_schema(BaseModel):
    movie_id:UUID = Field(default_factory=uuid4)
    title:str
    description:str
    language:str
    release_date:datetime
    director:str
    genres:List[Genre_schema]
    ratings:list[Review_schema]
    
    class Config:
        orm_mode=True  
class Get_rating(BaseModel):
    created_timestamp:datetime
    rating_id:UUID = Field(default_factory=uuid4)
    movie_id:UUID = Field(default_factory=uuid4)
    stars:float
    comments:str
    movie=Movie_response_schema
    class Config:
        orm_mode=True

          
class Get_movie_response_schema(BaseModel):
    # name:str
    movie_id:UUID = Field(default_factory=uuid4)
    title:str
    description:str
    language:str
    release_date:datetime
    director:str
    genres:List[Genre_schema]
    ratings:List[Rating]
    
    class Config:
        orm_mode=True
        
class Test(BaseModel):
    Rating:Review_schema
    Movie:Movie_response_schema
    
    class Config:
        orm_mode=True
        
class Test2(BaseModel):
    Rating:Test
    
    class Config:
        orm_mode=True