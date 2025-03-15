-- Insert into users table
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (1, 'user1@example.com', 'hashedpassword', 'patient');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (2, 'user2@example.com', 'hashedpassword', 'patient');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (3, 'user3@example.com', 'hashedpassword', 'patient');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (4, 'user4@example.com', 'hashedpassword', 'patient');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (5, 'user5@example.com', 'hashedpassword', 'patient');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (6, 'user6@example.com', 'hashedpassword', 'doctor');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (7, 'user7@example.com', 'hashedpassword', 'doctor');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (8, 'user8@example.com', 'hashedpassword', 'doctor');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (9, 'user9@example.com', 'hashedpassword', 'pharmacy_admin');
INSERT INTO users (user_id, email, password_hash, user_type) VALUES (10, 'user10@example.com', 'hashedpassword', 'pharmacy_admin');

-- Insert into pharmacies table
INSERT INTO pharmacies (pharmacy_id, admin_user_id, name, address, zip_code, phone_number, license_number, is_active) VALUES (1, 9, 'Pharmacy 1', '123 Pharmacy St, City 1', '90978', '555-01', 'LIC1', True);
INSERT INTO pharmacies (pharmacy_id, admin_user_id, name, address, zip_code, phone_number, license_number, is_active) VALUES (2, 2, 'Pharmacy 2', '123 Pharmacy St, City 2', '25719', '555-02', 'LIC2', True);
INSERT INTO pharmacies (pharmacy_id, admin_user_id, name, address, zip_code, phone_number, license_number, is_active) VALUES (3, 10, 'Pharmacy 3', '123 Pharmacy St, City 3', '66552', '555-03', 'LIC3', True);

-- Insert into patients table
INSERT INTO patients (patient_id, user_id, first_name, last_name, address, phone_number, zip_code, is_active) VALUES (1, 1, 'David', 'Williams', '123 Patient St', '555-1234', '10001', True);
INSERT INTO patients (patient_id, user_id, first_name, last_name, address, phone_number, zip_code, is_active) VALUES (2, 4, 'Bob', 'Brown', '123 Patient St', '555-1234', '10001', True);
INSERT INTO patients (patient_id, user_id, first_name, last_name, address, phone_number, zip_code, is_active) VALUES (3, 2, 'Alice', 'Brown', '123 Patient St', '555-1234', '10001', True);
INSERT INTO patients (patient_id, user_id, first_name, last_name, address, phone_number, zip_code, is_active) VALUES (4, 3, 'David', 'Johnson', '123 Patient St', '555-1234', '10001', True);
INSERT INTO patients (patient_id, user_id, first_name, last_name, address, phone_number, zip_code, is_active) VALUES (5, 5, 'David', 'Jones', '123 Patient St', '555-1234', '10001', True);

-- Insert into medical_metrics table
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (1, 1, 78.56, 1.89, 2167, '2025-03-07 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (2, 1, 84.14, 1.74, 1802, '2025-01-16 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (3, 1, 59.29, 1.62, 1770, '2025-01-08 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (4, 2, 93.47, 1.89, 2304, '2025-02-04 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (5, 2, 90.09, 1.53, 2475, '2025-02-22 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (6, 2, 89.78, 1.96, 1804, '2024-12-29 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (7, 3, 76.74, 1.89, 1733, '2024-12-31 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (8, 3, 94.33, 1.84, 1889, '2025-03-08 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (9, 3, 79.21, 1.77, 1637, '2025-03-09 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (10, 4, 75.21, 1.85, 1714, '2024-12-26 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (11, 4, 70.52, 1.91, 1842, '2024-12-07 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (12, 4, 60.32, 1.66, 1770, '2024-12-05 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (13, 5, 57.18, 1.98, 2328, '2025-02-21 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (14, 5, 60.04, 1.79, 2234, '2025-01-04 04:17:52');
INSERT INTO medical_metrics (metric_id, patient_id, weight, height, caloric_intake, recorded_at) VALUES (15, 5, 63.47, 1.51, 2015, '2025-02-25 04:17:52');

-- Insert into doctors table
INSERT INTO doctors (doctor_id, user_id, license_number, first_name, last_name, address, phone_number, ssn, is_active) VALUES (1, 8, 'DOC1', 'Alice', 'Brown', '123 Doctor St', '555-5678', '312451926', True);
INSERT INTO doctors (doctor_id, user_id, license_number, first_name, last_name, address, phone_number, ssn, is_active) VALUES (2, 6, 'DOC2', 'David', 'Jones', '123 Doctor St', '555-5678', '103152140', True);
INSERT INTO doctors (doctor_id, user_id, license_number, first_name, last_name, address, phone_number, ssn, is_active) VALUES (3, 7, 'DOC3', 'Bob', 'Johnson', '123 Doctor St', '555-5678', '764214692', True);
