from datetime import datetime
from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from database import SessionLocal,get_db
from models import Rating, User,Movie,Genre,Watched,Subscription
from schemas import Movie_response_schema, Test, Watch,Review_schema,Get_movie_response_schema,Get_rating
from JWTtoken import get_current_user
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from fastapi.security import OAuth2PasswordRequestForm
from hashing import Hash
from JWTtoken import create_access_token
import pickle
############################################################################################

router=APIRouter(
    tags=["User"],
    prefix="/user"
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm=Depends(),db:SessionLocal=Depends(get_db)):
    user=db.query(User).filter(User.email==request.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    access_token =(create_access_token(data={"sub": user.email}))
    #Save the variable
    pickle.dump(access_token, open("variableStoringFile.dat", "wb"))
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/get/movie/all",response_model=List[Get_movie_response_schema])
def view_all_movies(db:SessionLocal=Depends(get_db)):
    movies=db.query(Movie).all()
    return movies

@router.get("/get/movie",response_model=Get_movie_response_schema)
def search_movie(title,db:SessionLocal=Depends(get_db),current_user: Watch = Depends(get_current_user)):
    movie=db.query(Movie).filter(Movie.title==title).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No movies with the title {title}")
    # getting current user
    access_token = pickle.load(open("variableStoringFile.dat", "rb"))
    user=jwt.decode(token=access_token,key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    user=db.query(User).filter(User.email==user['sub']).first()
    
    k=[movie]+[movie.genres]+[movie.ratings]
    
    return k[0]

@router.get("/get/movie/genre")
def search_genre(genre,db:SessionLocal=Depends(get_db),current_user: Watch = Depends(get_current_user)):
    genreObj=db.query(Genre).filter(Genre.genre_name==genre).first()
    # movies=db.query()
    if not genreObj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No movies with the genre {genre}")
    
    return genreObj.movies 



@router.post("/watch")
def watch(request:Watch,db:SessionLocal=Depends(get_db),current_user: Watch = Depends(get_current_user)):
    movie=db.query(Movie).filter(Movie.title==request.title).first()
    if not movie:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Please enter a valid title")
    
    #Load the variable
    access_token = pickle.load(open("variableStoringFile.dat", "rb"))
    user=jwt.decode(token=access_token,key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    
    user=db.query(User).filter(User.email==user['sub']).first()
    
    #checking the subscription of the current user
    expObj=db.query(Subscription).filter(Subscription.user_id==user.user_id).first()
    current=str(datetime.utcnow()).split(" ")
    end=str(expObj.end_timestamp).split(" ")
    if current>end :
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,detail="Subscription Expired")
    watched_users=db.query(Watched).filter(Watched.user_id==user.user_id).all()
    k=0
    for i in watched_users:
        if (i.movie_id)==(movie.movie_id):
            k=k+1   
    watch=Watched(user_id=user.user_id,movie_id=movie.movie_id)
    db.add(watch)
    db.commit()
    db.refresh(watch)
    return f"You have watched {request.title} {k+1} times",watch


@router.post("/review")
def review(request:Review_schema,db:SessionLocal=Depends(get_db),current_user: Watch = Depends(get_current_user)):
    movie=db.query(Movie).filter(Movie.title==request.title).first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please enter a valid movie title")
    # getting current user
    access_token = pickle.load(open("variableStoringFile.dat", "rb"))
    user=jwt.decode(token=access_token,key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    
    user=db.query(User).filter(User.email==user['sub']).first()
    #checking if the user has watched a movie or not
    watched_users=db.query(Watched).filter(Watched.user_id==user.user_id).all()
    watch=0
    for i in watched_users:
        if (i.movie_id)==(movie.movie_id):
            watch=1
            break
    
    
    if watch==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Please watch the movie {movie.title} before writing a review")
    if request.stars<0 or request.stars>10:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Please give stars in the range of [0 to 10]")
    #getting all details from Ratings table by user_id, check corresponding movie id of user, 
    # if corresponding movie_id is equal to movie_id of reviewing movie raise exception
    ratings_of_current_user=db.query(Rating).filter(Rating.user_id==user.user_id).all()
    for i in ratings_of_current_user:
        if i.movie_id==movie.movie_id:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="You can only write one review, please edit the existing review if you want to make any changes")
    
    review=Rating(user_id=user.user_id,movie_id=movie.movie_id,stars=request.stars,comments=request.comments)
    # return user.ratings
    db.add(review)
    db.commit()
    db.refresh(review)
    return "submitted review sucessfully",review


@router.get("/get/reviews",response_model=List[Test])
def my_reviews(db:SessionLocal=Depends(get_db),current_user: Rating = Depends(get_current_user)):
    # getting current user
    access_token = pickle.load(open("variableStoringFile.dat", "rb"))
    user=jwt.decode(token=access_token,key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    user=db.query(User).filter(User.email==user['sub']).first()
    
    rating=db.query(Rating).filter(Rating.user_id==user.user_id).all()
    res=db.query(Movie.title,Rating).outerjoin(Rating,Movie.movie_id==Rating.movie_id).filter(Rating.user_id==user.user_id).all()
    # mov_names=[Rating()]
    # for i in rating:
        
    #     mov_names.append(i.movie)
    # mov_names.pop(0)
    
    if not user.ratings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No reviews, please write a review")
    return res#user.ratings


@router.put("/review/edit")
def edit_my_review(request:Review_schema,db:SessionLocal=Depends(get_db),current_user: Rating = Depends(get_current_user)):
     # getting current user
    access_token = pickle.load(open("variableStoringFile.dat", "rb"))
    user=jwt.decode(token=access_token,key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    user=db.query(User).filter(User.email==user['sub']).first()
    
    movie=db.query(Movie).filter(Movie.title==request.title).first()
    reviews=db.query(Rating).filter(Rating.user_id==user.user_id).all()
    for i in reviews:
        if i.movie_id==movie.movie_id:
            if request.stars<0 or request.stars>10:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"Please give stars in the range of [0 to 10]")
            i.stars=request.stars
            i.comments=request.comments
            
    db.commit()
    review=db.query(Rating).filter(Rating.movie_id==movie.movie_id).first()
    return "Updated review:",review


@router.delete("/movie/review/delete")
def delete_my_review(title,db:SessionLocal=Depends(get_db),current_user: Movie = Depends(get_current_user)):
    movie=db.query(Movie).filter(Movie.title==title).first()
    if not movie:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"movie with title {title} not found")
        
    review=db.query(Rating).filter(Rating.movie_id==movie.movie_id).delete(synchronize_session=False)
    db.commit()
    return f"Sucessfully deleted your review on movie {title}"
    
