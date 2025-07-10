import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db, get_sessionmaker
from app.main import app

# Используем SQLite in-memory БД для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Создаем отдельный engine и сессию для тестов
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = get_sessionmaker(test_engine)


@pytest.fixture(scope="session")
def db_engine():
    """Создание всех таблиц перед тестами и удаление после."""
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Создание новой сессии для каждого теста."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Переопределяем зависимость get_db в FastAPI."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
