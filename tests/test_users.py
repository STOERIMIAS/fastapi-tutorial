from app import schemas
from .database import client, session

def test_root(client):
    res = client.get("/")
    assert res.json().get('Hello') == "welcome to my API"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "password1234"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "password1234"})
    res = client.post("/login", data={"username": "test@gmail.com", "password": "password1234"})
    print(res.json())
    assert res.status_code == 200