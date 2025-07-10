CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    telegram_id BIGINT
);

CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
    patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    description TEXT,
    UNIQUE (doctor_id, start_time)
);

-- Тестовые данные 
INSERT INTO doctors (name, specialty)
VALUES 
    ('Dr. House', 'Diagnostics'),
    ('Dr. Watson', 'General Practice');

INSERT INTO patients (name, telegram_id)
VALUES 
    ('Greg Patient', 5550001),
    ('John Smith', 5550002);

INSERT INTO appointments (doctor_id, patient_id, start_time, end_time, description)
VALUES
    (1, 1, '2025-01-01 09:00:00', '2025-01-01 09:30:00', 'Initial consult'),
    (2, 2, '2025-01-02 10:00:00', '2025-01-02 10:45:00', 'Follow-up');