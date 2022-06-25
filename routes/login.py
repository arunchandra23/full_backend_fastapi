from fastapi import APIRouter,Depends,HTTPException,status
from models import User
from schemas import Login
from database import SessionLocal,get_db
from hashing import Hash
from JWTtoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm




router=APIRouter(
    tags=["Login"]
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm=Depends(),db:SessionLocal=Depends(get_db)):
    user=db.query(User).filter(User.email==request.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
