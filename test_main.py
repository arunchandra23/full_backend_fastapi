from fastapi.testclient import TestClient
from main import app


client= TestClient(app)

user_data ={
  "name": "test2",
  "email": "test2@gmail.com",
  "password": "test2",
  "subscription_expires": "2022-07-28T10:56:52.135Z"
}

genre_data={
  "genre_name":"horror"
}

movie_data=  {
  "title": "baahubali 5",
  "description": "part 3",
  "language": "telugu,hindi",
  "release_date": "2022-06-29T04:51:35.053Z",
  "director": "rajamouli",
  "genres": [
    "action"
  ]
}

def test_add_user():
  response=client.post("/add/user",json=user_data)
  assert response.status_code==200
    
def test_add_genre():
  response=client.post("/add/genre",json=genre_data)
  assert response.status_code==200
  
def test_add_movie():
  response=client.post("/add/movie",json=movie_data)
  response.status_code==200
  
