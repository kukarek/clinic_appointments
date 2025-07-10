import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .db import SessionLocal

logger = logging.getLogger(__name__)
router = APIRouter()


def get_db():
    """
    Генератор сессии БД.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/appointments", response_model=schemas.Appointment)
def create(data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    """
    Создать новую запись на приём.

    Args:
        data (schemas.AppointmentCreate): Данные новой записи.
        db (Session): Сессия базы данных.

    Returns:
        schemas.Appointment: Созданная запись.

    Raises:
        HTTPException 400: Ошибка при создании записи (например, если врач занят).
    """
    logger.info(
        f"Создание записи: доктор_id={data.doctor_id}, пациент_id={data.patient_id}, "
        f"start_time={data.start_time}, end_time={data.end_time}"
    )
    try:
        appointment = crud.create_appointment(db, data)
        logger.info(f"Запись создана с id={appointment.id}")
        return appointment
    except ValueError as e:
        logger.error(f"Ошибка при создании записи: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
def read(appointment_id: int, db: Session = Depends(get_db)):
    """
    Получить запись по ID.

    Args:
        appointment_id (int): ID записи.
        db (Session): Сессия базы данных.

    Returns:
        schemas.Appointment: Найденная запись.

    Raises:
        HTTPException 404: Если запись не найдена.
    """
    logger.info(f"Запрос записи с id={appointment_id}")
    appointment = crud.get_appointment(db, appointment_id)
    if not appointment:
        logger.warning(f"Запись с id={appointment_id} не найдена")
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
