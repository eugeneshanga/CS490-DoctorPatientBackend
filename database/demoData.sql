USE weight_loss_clinic;

-- Insert users
INSERT INTO users (email, password_hash, user_type) VALUES
('jane.doe@example.com', '$2b$12$gNhYhBS1n66b3YrhFD94neI5AlOiw98vi.S7TCS.5HB8.0cCoAtyy', 'patient'),
('dr.smith@example.com', '$2b$12$mJcqyCWMyyj7I9xiSz8cHO66SlD6ByAx/6Xnudg0f8KZH3JwyNbke', 'doctor'),
('goodhealthrx@example.com', '$2b$12$QKo92f1qMctTcsL3qXzWh.N.j2pX0ObB71vtKCDZux0F1rFli3uCO', 'pharmacy'),
('citymeds@example.com',    '$2b$12$QKo92f1qMctTcsL3qXzWh.N.j2pX0ObB71vtKCDZux0F1rFli3uCO', 'pharmacy'),
('neighborhoodpharm@example.com', '$2b$12$QKo92f1qMctTcsL3qXzWh.N.j2pX0ObB71vtKCDZux0F1rFli3uCO', 'pharmacy'),
('dr.jones@example.com', '$2b$12$PU2bIEsqAbSRYpsaUmt1LelQDOQZqMgxAmkR9B81PCH5Ra2dubbhy', 'doctor'),
('dr.lee@example.com',  '$2b$12$zvxJm/HBicsnZDP1Zfstiu0UGz7H679c0CgyHK/lZGtkuKCezJewW', 'doctor'),
('dr.brown@example.com', '$2b$12$SgQR2JV3iLekKSQ8QO8AeOlgDW3OYDX2FL4RkgOiduKrkFYP/j7Sq', 'doctor');

-- Insert patient
INSERT INTO patients (user_id, first_name, last_name, address, phone_number, zip_code) VALUES
(1, 'Jane', 'Doe', '123 Elm Street', '555-1234', '10001');

-- Insert doctor
INSERT INTO doctors (user_id, license_number, first_name, last_name, address, phone_number, ssn) VALUES
(2, 'DOC123456', 'John', 'Smith', '456 Oak Avenue', '555-5678', '123-45-6789'),
(6, 'DOC222333', 'Alice',  'Jones', '234 Birch Lane',   '555-3456', '234-56-7890'),
(7, 'DOC444555', 'Robert', 'Lee',   '345 Maple Street', '555-4567', '345-67-8901'),
(8, 'DOC777888', 'Emily', 'Brown', '678 Cedar Avenue', '555-7777', '987-65-4321');

-- Insert pharmacy
INSERT INTO pharmacies (user_id, name, address, zip_code, phone_number, license_number) VALUES
(3, 'GoodHealth Pharmacy', '789 Pine Road', '10002', '555-9012', 'PHARM99999'),
(4, 'CityMeds Pharmacy', '101 Main Street', '10010', '555-2222', 'PHARM10010'),
(5, 'Neighborhood Pharmacy', '202 Oak Boulevard', '07001', '555-3333', 'PHARM07001');

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
(1, 1, NOW() - INTERVAL 10 DAY, 'completed'),
(1, 1, NOW() - INTERVAL  5 DAY, 'completed'),
(1, 1, NOW() - INTERVAL 5 DAY, 'canceled'),
(2, 1, NOW() - INTERVAL  8 DAY, 'completed'),
(3, 1, NOW() - INTERVAL  6 DAY, 'completed'),
(4, 1, NOW() - INTERVAL  2 DAY, 'completed');

-- Insert payments to doctor
INSERT INTO payments_doctor (doctor_id, patient_id, amount, is_fulfilled) VALUES
(1, 1, 100.00, TRUE),
(1, 1, 120.00, FALSE);

-- Insert payments to pharmacy
INSERT INTO payments_pharmacy (pharmacy_id, patient_id, amount, is_fulfilled) VALUES
(1, 1, 45.50, TRUE),
(1, 1, 60.75, FALSE);

INSERT INTO patient_preferred_pharmacy (patient_id, pharmacy_id)
VALUES (1, 3);

INSERT INTO ratings (patient_id, doctor_id, appointment_id, rating, review) VALUES
(1, 1,             1, 4.5, 'Fantastic care by Dr. Smith'),
(1, 1,             2, 3.5, 'Good, but felt rushed'),
(1, 2,             3,  5.0, 'Dr. Jones was thorough and kind'),
(1, 3,             4,    3.5, 'Very helpful advice'),
(1, 4,   5,  4.5, 'Dr. Brown was outstanding');

TRUNCATE TABLE doctor_ratings;
INSERT INTO doctor_ratings (doctor_id, total_ratings, average_rating)
SELECT
  doctor_id,
  COUNT(*)        AS total_ratings,
  ROUND(AVG(rating), 2) AS average_rating
FROM ratings
GROUP BY doctor_id;
