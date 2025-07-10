from datetime import datetime

from app import crud, models


def test_create_doctor(db_session):
    doctor_in = models.Doctor(name="Dr. Smith", specialty="Cardiology")
    db_session.add(doctor_in)
    db_session.commit()
    db_session.refresh(doctor_in)

    assert doctor_in.id is not None
    assert doctor_in.name == "Dr. Smith"


def test_create_patient(db_session):
    patient_in = models.Patient(name="John Doe", telegram_id="1234567890")
    db_session.add(patient_in)
    db_session.commit()
    db_session.refresh(patient_in)

    assert patient_in.id is not None
    assert patient_in.name == "John Doe"


def test_create_appointment(db_session):
    doctor = models.Doctor(name="Dr. Who")
    patient = models.Patient(name="Jane Roe")
    db_session.add_all([doctor, patient])
    db_session.commit()
    db_session.refresh(doctor)
    db_session.refresh(patient)

    appointment_in = models.Appointment(
        doctor_id=doctor.id,
        patient_id=patient.id,
        start_time=datetime(2025, 1, 1, 10, 0, 0),
        end_time=datetime(2025, 1, 1, 10, 30, 0),
        description="Checkup",
    )
    db_session.add(appointment_in)
    db_session.commit()
    db_session.refresh(appointment_in)

    assert appointment_in.id is not None
    assert appointment_in.doctor_id == doctor.id
    assert appointment_in.patient_id == patient.id
