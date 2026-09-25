from app import schemas
from app.config import settings
import pytest
import jwt

def test_create_user(client):
    res = client.post("/users/", json={"email": "test@gmail.com", "password": "password1234"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201

    res = client.post("/users/", json={"email": "test@gmail.com", "password": "password1234"})
    assert res.status_code == 409

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: int = payload.get("user_id")
    email: str = payload.get("email")
    assert id == test_user["id"]
    assert email == test_user["email"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password1234', 401),
    ('test@gmail.com', 'wrongpassword', 401),
    ('wrongemail@gmail.com', 'wrongpassword', 401),
    (None, 'password1234', 422),
    ('test@gmail.com', None, 422)
])

def test_incorrect_login_user(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    
    assert res.status_code == status_code


