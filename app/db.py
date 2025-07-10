import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

logger = logging.getLogger(__name__)
load_dotenv(".env")

# Базовый класс для моделей
Base = declarative_base()

# --- Конфигурация подключения ---
DB_USER = os.getenv("DB_USER", "clinic_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "clinic_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "clinic_db")

DEFAULT_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# --- Создание движка с логированием ---
def get_engine(database_url: str | None = None):
    url = database_url or DEFAULT_DATABASE_URL
    logger.info(f"Connecting to database at {url}")
    return create_engine(url, pool_pre_ping=True)


# --- Создание SessionLocal от конкретного движка ---
def get_sessionmaker(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Основной движок и сессия ---
engine = get_engine()
SessionLocal = get_sessionmaker(engine)


# --- Зависимость FastAPI для получения БД-сессии ---
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
