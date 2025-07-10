Вот упрощённая и более понятная версия `README.md` — без перегрузки терминами, но с сохранением всей нужной информации:

---

## 🏥 Clinic Appointments

Микросервис на FastAPI для записи пациентов на приём к врачу.
Разворачивается за 1 минуту через Docker. Поддерживает API, тесты, CI, .env и сценарий Telegram-бота.

---

## 🚀 Быстрый запуск

```bash
git clone https://github.com/kukarek/clinic_appointments.git
cd clinic-appointments
cp .env.example .env
make up
```

Открой в браузере: [http://localhost:8000](http://localhost:8000)
Проверка сервиса: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🔧 Примеры API

```bash

# Новая запись
curl -X POST http://localhost:8000/appointments \
 -H "Content-Type: application/json" \
 -d '{
     "doctor_id": 1,
     "patient_name": "John Doe",
     "start_time": "2025-01-01T10:00:00",
     "end_time": "2025-01-01T10:30:00",
     "description": "Checkup"
 }'

# Получить запись
curl http://localhost:8000/appointments/1
```

---

## 🛠️ Что внутри

* FastAPI, Pydantic, SQLAlchemy
* PostgreSQL (через docker-compose)
* Makefile для удобства
* Тесты на pytest
* Линтеры (black, isort, flake8)
* CI на GitHub Actions

---

## 📂 Основные команды

```bash
make up      # запуск проекта
make down    # остановка
make lint    # форматирование и проверка кода
make test    # запуск тестов
```

---

## 📋 Структура базы

```
doctors
-------
id (PK)
name (str)
specialty (str)

patients
--------
id (PK)
name (str)
telegram_id (int)

appointments
------------
id (PK)
doctor_id (FK -> doctors.id)
patient_id (FK -> patients.id)
start_time (datetime)
end_time (datetime)
description (text)
UNIQUE(doctor_id, start_time)

```

## ✅ CI / Проверки

* При пуше запускается GitHub Actions
* Выполняет:

  * `make lint`
  * `make test`
* Использует PostgreSQL-сервис




