import logging

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schemas

logger = logging.getLogger(__name__)


def get_doctor(db: Session, doctor_id: int) -> models.Doctor | None:
    """
    Получить врача по его ID.

    Args:
        db (Session): Сессия базы данных.
        doctor_id (int): Идентификатор врача.

    Returns:
        models.Doctor | None: Объект врача, если найден, иначе None.
    """
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    logger.debug(f"Получен врач с id={doctor_id}: {doctor}")
    return doctor


def create_doctor(db: Session, doctor: schemas.DoctorCreate) -> models.Doctor:
    """
    Создать нового врача.

    Args:
        db (Session): Сессия базы данных.
        doctor (schemas.DoctorCreate): Данные для создания врача.

    Returns:
        models.Doctor: Созданный объект врача.
    """
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    logger.info(f"Создан врач с id={db_doctor.id}")
    return db_doctor


def get_patient(db: Session, patient_id: int) -> models.Patient | None:
    """
    Получить пациента по его ID.

    Args:
        db (Session): Сессия базы данных.
        patient_id (int): Идентификатор пациента.

    Returns:
        models.Patient | None: Объект пациента, если найден, иначе None.
    """
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    logger.debug(f"Получен пациент с id={patient_id}: {patient}")
    return patient


def create_patient(db: Session, patient: schemas.PatientCreate) -> models.Patient:
    """
    Создать нового пациента.

    Args:
        db (Session): Сессия базы данных.
        patient (schemas.PatientCreate): Данные для создания пациента.

    Returns:
        models.Patient: Созданный объект пациента.
    """
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    logger.info(f"Создан пациент с id={db_patient.id}")
    return db_patient


def create_appointment(
    db: Session, appointment: schemas.AppointmentCreate
) -> models.Appointment:
    """
    Создать новую запись на приём.

    Args:
        db (Session): Сессия базы данных.
        appointment (schemas.AppointmentCreate): Данные для создания записи.

    Raises:
        HTTPException: Если врач уже занят в это время (IntegrityError).

    Returns:
        models.Appointment: Созданная запись на приём.
    """
    # Проверка: start_time < end_time
    if appointment.start_time >= appointment.end_time:
        logger.warning(
            f"Invalid appointment times: start_time {appointment.start_time} >= end_time {appointment.end_time}"
        )
        raise HTTPException(
            status_code=400,
            detail="Начальное время должно быть меньше конечного времени",
        )

    # Проверка перекрытия по времени у врача
    conflict = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == appointment.doctor_id,
            # Пересечение интервалов:
            and_(
                models.Appointment.start_time < appointment.end_time,
                models.Appointment.end_time > appointment.start_time,
            ),
        )
        .first()
    )
    if conflict:
        logger.warning(
            f"Doctor {appointment.doctor_id} busy at {appointment.start_time} - {appointment.end_time}"
        )
        raise HTTPException(status_code=400, detail="Врач уже занят в это время")

    # Если все проверки пройдены — создаём запись
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"DB commit error: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании записи")
    db.refresh(db_appointment)
    logger.info(
        f"Appointment created: {db_appointment.id} for doctor {appointment.doctor_id}"
    )
    return db_appointment


def get_appointment(db: Session, appointment_id: int) -> models.Appointment | None:
    """
    Получить запись на приём по её ID.

    Args:
        db (Session): Сессия базы данных.
        appointment_id (int): Идентификатор записи на приём.

    Returns:
        models.Appointment | None: Объект записи, если найден, иначе None.
    """
    appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.id == appointment_id)
        .first()
    )
    logger.debug(f"Получена запись на приём с id={appointment_id}: {appointment}")
    return appointment
