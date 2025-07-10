from app import models


def test_full_flow(client, db_session):
    # Создаем доктора напрямую
    doctor = models.Doctor(name="Dr. House", specialty="Diagnostics")
    db_session.add(doctor)

    # Создаем пациента напрямую
    patient = models.Patient(name="Greg Patient", telegram_id="123456")
    db_session.add(patient)

    db_session.commit()
    db_session.refresh(doctor)
    db_session.refresh(patient)

    # Создаем запись через ручку
    appointment_resp = client.post(
        "/appointments/",
        json={
            "doctor_id": doctor.id,
            "patient_id": patient.id,
            "start_time": "2025-12-01T09:00:00",
            "end_time": "2025-12-01T09:30:00",
            "description": "Initial consult",
        },
    )
    assert appointment_resp.status_code == 200
    appt_id = appointment_resp.json()["id"]

    # Получаем запись через ручку
    get_resp = client.get(f"/appointments/{appt_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["doctor"]["id"] == doctor.id
    assert data["patient"]["id"] == patient.id
    assert data["description"] == "Initial consult"
