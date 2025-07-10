from datetime import datetime

from pydantic import BaseModel


class DoctorBase(BaseModel):
    """
    Базовая схема врача.

    Attributes:
        name (str): Имя врача.
        specialty (str | None): Специализация врача, необязательное поле.
    """

    name: str
    specialty: str | None = None


class DoctorCreate(DoctorBase):
    """Схема создания врача (наследует DoctorBase)."""

    pass


class Doctor(DoctorBase):
    """
    Схема врача с ID (используется для ответа).

    Attributes:
        id (int): Идентификатор врача.
    """

    id: int

    class Config:
        from_attributes = True


class PatientBase(BaseModel):
    """
    Базовая схема пациента.

    Attributes:
        name (str): Имя пациента.
        phone (str | None): Телефон пациента, необязательное поле.
    """

    name: str
    telegram_id: int | None = None


class PatientCreate(PatientBase):
    """Схема создания пациента (наследует PatientBase)."""

    pass


class Patient(PatientBase):
    """
    Схема пациента с ID (для ответа).

    Attributes:
        id (int): Идентификатор пациента.
    """

    id: int

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    """
    Базовая схема записи на приём.

    Attributes:
        doctor_id (int): ID врача.
        patient_id (int): ID пациента.
        start_time (datetime): Время начала приёма.
        end_time (datetime): Время окончания приёма.
        description (str | None): Описание, необязательное поле.
    """

    doctor_id: int
    patient_id: int
    start_time: datetime
    end_time: datetime
    description: str | None = None


class AppointmentCreate(AppointmentBase):
    """Схема создания записи (наследует AppointmentBase)."""

    pass


class Appointment(AppointmentBase):
    """
    Схема записи с деталями врача и пациента (для ответа).

    Attributes:
        id (int): Идентификатор записи.
        doctor (Doctor): Вложенный объект врача.
        patient (Patient): Вложенный объект пациента.
    """

    id: int
    doctor: Doctor
    patient: Patient

    class Config:
        from_attributes = True
