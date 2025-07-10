from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from .db import Base


class Doctor(Base):
    """
    Модель врача.

    Attributes:
        id (int): Уникальный идентификатор врача.
        name (str): Имя врача.
        specialty (str | None): Специализация врача.
        appointments (List[Appointment]): Связанные записи приёмов.
    """

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=True)

    appointments = relationship("Appointment", back_populates="doctor")


class Patient(Base):
    """
    Модель пациента.

    Attributes:
        id (int): Уникальный идентификатор пациента.
        name (str): Имя пациента.
        telegram_id (int | None): Телеграм пациента.
        appointments (List[Appointment]): Связанные записи приёмов.
    """

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    telegram_id = Column(Integer, nullable=True)

    appointments = relationship("Appointment", back_populates="patient")


class Appointment(Base):
    """
    Модель записи на приём.

    Attributes:
        id (int): Уникальный идентификатор записи.
        doctor_id (int): Внешний ключ на врача.
        patient_id (int): Внешний ключ на пациента.
        start_time (datetime): Время начала приёма.
        end_time (datetime): Время окончания приёма.
        description (str | None): Описание или заметки.
        doctor (Doctor): Объект врача.
        patient (Patient): Объект пациента.
    """

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    description = Column(Text)

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")

    __table_args__ = (
        UniqueConstraint("doctor_id", "start_time", name="unique_doctor_start_time"),
    )
