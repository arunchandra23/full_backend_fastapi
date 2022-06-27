from fastapi import APIRouter,Depends,HTTPException,status
from database import SessionLocal,get_db
from models import User,Movie,Genre,Subscription
from schemas import Movie_schema, User_response_schema, User_schema,Genre_schema,Movie_response_schema
from hashing import Hash
from JWTtoken import get_current_user



router=APIRouter(
    tags=["Admin"],
    prefix="/add"
)

@router.post("/user",response_model=User_response_schema)
def add_user(request:User_schema,db:SessionLocal=Depends(get_db)):#,current_user: User_schema = Depends(get_current_user)
    user= User(name=request.name,email=request.email,password=Hash.hash(request.password))
    subs=Subscription(end_timestamp=request.subscription_expires)
    db.add(subs)
    db.commit()
    db.refresh(subs)
    # s=db.query(Subscription).filter(Subscription.end_timestamp==request.subscription_expires).first()
    if not user:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,detail="Failed to add user")
    user.subscription.append(subs)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/genre")
def add_genre(request:Genre_schema,db:SessionLocal=Depends(get_db)):
    genre= Genre(genre_name=request.genre_name.lower())
    if not genre:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,detail="Failed to add genre")
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


@router.post("/movie",response_model=Movie_response_schema)
def add_movie(request:Movie_schema,db:SessionLocal=Depends(get_db)):
    movie= Movie(title=request.title.lower(),description=request.description,language=request.language.lower(),release_date=request.release_date,director=request.director)
    genres=request.genres
    languages=["telugu","hindi","english","tamil","kannada","marathi","urdu"]
    k=0
    req=request.language.split(",")
    l=len(req)
    for i in languages:
        for j in req:
            if i.lower()==j.lower():
                k=k+1
                break
            
    if k!=l:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Please enter a valid language")
    for genre in genres:
        g=db.query(Genre).filter(Genre.genre_name==genre.lower()).first()
        if not g:
            raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Please enter a valid genre")
        movie.genres.append(g)

    if not movie:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,detail="Failed to add movie")
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie
    