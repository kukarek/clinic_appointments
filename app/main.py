import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from . import db, models
from .routes import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекст жизненного цикла приложения FastAPI.

    Логирует запуск и завершение приложения,
    а также создает таблицы в базе данных при старте.
    """
    logger.info("Starting up: creating database tables if not exist")
    models.Base.metadata.create_all(bind=db.engine)
    logger.info("Database tables created (if not exist)")
    yield
    logger.info("Shutting down application")


app = FastAPI(title="Clinic Appointments API", lifespan=lifespan)
app.include_router(router)


@app.get("/health", tags=["Health"])
def health():
    """
    Эндпоинт проверки состояния сервиса.

    Returns:
        dict: {"status": "ok"}
    """
    logger.info("Health check endpoint called")
    return {"status": "ok"}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),  # вывод в консоль
        ],
    )
    logger.info("Starting application with uvicorn")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
