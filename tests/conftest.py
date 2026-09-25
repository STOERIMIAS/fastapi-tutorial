from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
import pytest
from pathlib import Path
from alembic import command
from alembic.config import Config
from app.oauth2 import create_access_token
from app import models

#conftest ist ordner spezifisch und funktioniert in allen ordner in diesem Ornder

#----------------------------------------------------------------------------------------------
# db fixture
#----------------------------------------------------------------------------------------------

postgres_url = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(postgres_url)
Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

alembic_cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)

@pytest.fixture(scope="function")
def session():
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close
    app.dependency_overrides[get_db] = get_test_db
    return TestClient(app)


#----------------------------------------------------------------------------------------------
# users fixture
#----------------------------------------------------------------------------------------------

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com", 
                 "password": "password1234"}
    res = client.post("/users/", json =user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

#----------------------------------------------------------------------------------------------
# Oaut2token fixture
#----------------------------------------------------------------------------------------------

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"], "email": test_user["email"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

#----------------------------------------------------------------------------------------------
# Posts fixture
#----------------------------------------------------------------------------------------------

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }]

    def creat_post_model(post):
        return models.Post(**post)

    post_map = map(creat_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts