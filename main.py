from fastapi import FastAPI
from routes import admin,user,login
from database import Base,engine

app = FastAPI()

Base.metadata.create_all(bind=engine)
# app.include_router(login.router)
app.include_router(admin.router)
app.include_router(user.router)