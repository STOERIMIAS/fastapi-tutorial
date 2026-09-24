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