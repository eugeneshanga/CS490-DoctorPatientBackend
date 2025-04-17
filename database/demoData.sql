USE weight_loss_clinic;

-- Insert users
INSERT INTO users (email, password_hash, user_type) VALUES
('jane.doe@example.com', '$2b$12$gNhYhBS1n66b3YrhFD94neI5AlOiw98vi.S7TCS.5HB8.0cCoAtyy', 'patient'),
('dr.smith@example.com', '$2b$12$mJcqyCWMyyj7I9xiSz8cHO66SlD6ByAx/6Xnudg0f8KZH3JwyNbke', 'doctor'),
('goodhealthrx@example.com', '$2b$12$QKo92f1qMctTcsL3qXzWh.N.j2pX0ObB71vtKCDZux0F1rFli3uCO', 'pharmacy');

-- Insert patient
INSERT INTO patients (user_id, first_name, last_name, address, phone_number, zip_code) VALUES
(1, 'Jane', 'Doe', '123 Elm Street', '555-1234', '10001');

-- Insert doctor
INSERT INTO doctors (user_id, license_number, first_name, last_name, address, phone_number, ssn) VALUES
(2, 'DOC123456', 'John', 'Smith', '456 Oak Avenue', '555-5678', '123-45-6789');

-- Insert pharmacy
INSERT INTO pharmacies (user_id, name, address, zip_code, phone_number, license_number) VALUES
(3, 'GoodHealth Pharmacy', '789 Pine Road', '10002', '555-9012', 'PHARM99999');

-- Doctor-Patient relationship
INSERT INTO doctor_patient (doctor_id, patient_id) VALUES (1, 1);

-- Insert 5 days of patient metrics
INSERT INTO medical_metrics (patient_id, weight, height, caloric_intake, recorded_at) VALUES
(1, 180.5, 65.0, 2000, NOW() - INTERVAL 4 DAY),
(1, 179.8, 65.0, 1950, NOW() - INTERVAL 3 DAY),
(1, 179.0, 65.0, 1900, NOW() - INTERVAL 2 DAY),
(1, 178.4, 65.0, 1800, NOW() - INTERVAL 1 DAY),
(1, 177.9, 65.0, 1750, NOW());

-- Insert appointments
INSERT INTO appointments (doctor_id, patient_id, appointment_time, status) VALUES
(1, 1, NOW() + INTERVAL 1 DAY, 'accepted'),
(1, 1, NOW() - INTERVAL 2 DAY, 'completed'),
(1, 1, NOW() - INTERVAL 5 DAY, 'canceled');

-- Insert payments to doctor
INSERT INTO payments_doctor (doctor_id, patient_id, amount, is_fulfilled) VALUES
(1, 1, 100.00, TRUE),
(1, 1, 120.00, TRUE);

-- Insert payments to pharmacy
INSERT INTO payments_pharmacy (pharmacy_id, patient_id, amount, is_fulfilled) VALUES
(1, 1, 45.50, TRUE),
(1, 1, 60.75, FALSE); -- example of a pending payment
