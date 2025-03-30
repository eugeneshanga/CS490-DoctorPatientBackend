-- USE the target database
USE weight_loss_clinic;

-- 1. Insert Users (for patients, doctors, and pharmacies)
INSERT INTO users (email, password_hash, user_type) VALUES
('patient1@example.com', 'hashed_pass1', 'patient'),
('patient2@example.com', 'hashed_pass2', 'patient'),
('patient3@example.com', 'hashed_pass3', 'patient'),
('doctor1@example.com', 'hashed_pass4', 'doctor'),
('doctor2@example.com', 'hashed_pass5', 'doctor'),
('doctor3@example.com', 'hashed_pass6', 'doctor'),
('pharmacy1@example.com', 'hashed_pass7', 'pharmacy');

-- 2. Insert Patients (Assuming the first three users are patients)
INSERT INTO patients (user_id, first_name, last_name, address, phone_number, zip_code, is_active) VALUES
(1, 'Alice', 'Johnson', '123 Apple St', '555-0101', '12345', TRUE),
(2, 'Bob', 'Smith', '456 Banana Ave', '555-0202', '23456', TRUE),
(3, 'Charlie', 'Brown', '789 Cherry Blvd', '555-0303', '34567', TRUE);

-- 3. Insert Doctors (Next three users are doctors)
INSERT INTO doctors (user_id, license_number, first_name, last_name, address, phone_number, ssn, is_active) VALUES
(4, 'LIC12345', 'Emily', 'Stone', '101 Doctor Rd', '555-1111', '111-11-1111', TRUE),
(5, 'LIC67890', 'Michael', 'Wright', '202 Medicine Ln', '555-2222', '222-22-2222', TRUE),
(6, 'LIC54321', 'Olivia', 'Carter', '303 Health Dr', '555-3333', '333-33-3333', TRUE);

-- 4. Insert Pharmacies (Last user is a pharmacy)
INSERT INTO pharmacies (user_id, name, address, zip_code, phone_number, license_number, is_active) VALUES
(7, 'Healthy Pharmacy', '111 Wellness Way', '45678', '555-4444', 'PHAR1234', TRUE);

-- 5. Insert Medical Metrics for Patients
INSERT INTO medical_metrics (patient_id, weight, height, caloric_intake) VALUES
(1, 65.5, 1.70, 2000),
(2, 82.3, 1.80, 2200),
(3, 74.0, 1.75, 2100);

-- 6. Insert Doctor-Patient Relationships
-- Assuming doctor_id values are auto-assigned as 1, 2, and 3 respectively.
INSERT INTO doctor_patient (doctor_id, patient_id) VALUES
(1, 1),  -- Dr. Emily (doctor_id=1) with Alice (patient_id=1)
(2, 2),  -- Dr. Michael (doctor_id=2) with Bob (patient_id=2)
(3, 3);  -- Dr. Olivia (doctor_id=3) with Charlie (patient_id=3)

-- 7. Insert Appointments
INSERT INTO appointments (doctor_id, patient_id, appointment_time, status) VALUES
(1, 1, '2025-04-10 09:00:00', 'scheduled'),
(2, 2, '2025-04-11 10:30:00', 'scheduled'),
(3, 3, '2025-04-12 14:00:00', 'scheduled');

-- 8. Insert Chat History
INSERT INTO chat_history (patient_id, doctor_id, message) VALUES
(1, 1, 'Hi Dr. Emily, I need to discuss my treatment.'),
(2, 2, 'Hello Dr. Michael, when can we schedule a follow-up?'),
(3, 3, 'Hi Dr. Olivia, I have some questions about my medication.');

-- 9. Insert Payments from Patients to Doctors
INSERT INTO payments_doctor (doctor_id, patient_id, amount, is_fulfilled) VALUES
(1, 1, 150.00, TRUE),
(2, 2, 200.00, FALSE),
(3, 3, 175.00, TRUE);

-- 10. Insert Payments from Patients to Pharmacy
INSERT INTO payments_pharmacy (pharmacy_id, patient_id, amount, is_fulfilled) VALUES
(1, 1, 30.00, TRUE),
(1, 2, 45.00, FALSE),
(1, 3, 50.00, TRUE);

-- 11. Insert Patient Meal Plans (using JSON for the meal_plan column)
INSERT INTO patient_meal_plans (patient_id, meal_plan) VALUES
(1, '{"breakfast": "Greek Yogurt with Fruit", "lunch": "Chicken Salad", "dinner": "Grilled Salmon"}'),
(2, '{"breakfast": "Oatmeal", "lunch": "Vegetable Stir-fry", "dinner": "Tofu Curry"}'),
(3, '{"breakfast": "Smoothie Bowl", "lunch": "Turkey Sandwich", "dinner": "Pasta Primavera"}');

-- 12. Insert Pharmacy Inventory
INSERT INTO pharmacy_inventory (pharmacy_id, drug_name, stock_quantity) VALUES
(1, 'Weight Loss Supplement', 100),
(1, 'Multivitamins', 200);

-- 13. Insert Discussion Board Posts (by Doctors)
INSERT INTO discussion_board (doctor_id, post_title, post_content) VALUES
(1, 'Nutrition Tips for Weight Loss', '{"content": "Eat more vegetables and lean protein."}'),
(2, 'Effective Workouts', '{"content": "Combine cardio and strength training for best results."}');

-- 14. Insert Replies to Discussion Board Posts (by Patients)
INSERT INTO post_replies (post_id, patient_id, reply_content) VALUES
(1, 2, 'Great advice, thank you!'),
(2, 3, 'I found this very helpful.');

-- 15. Insert Ratings for Appointments
INSERT INTO ratings (patient_id, doctor_id, appointment_id, rating, review) VALUES
(1, 1, 1, 4.5, 'Excellent consultation!'),
(2, 2, 2, 4.0, 'Very professional.'),
(3, 3, 3, 5.0, 'Outstanding service!');

-- 16. Insert Aggregated Doctor Ratings
INSERT INTO doctor_ratings (doctor_id, total_ratings, average_rating) VALUES
(1, 1, 4.5),
(2, 1, 4.0),
(3, 1, 5.0);

-- 17. Insert Prescriptions
INSERT INTO prescriptions (doctor_id, patient_id, pharmacy_id, medication_name, dosage, instructions, status) VALUES
(1, 1, 1, 'Medication A', '50mg', 'Take once daily', 'pending'),
(2, 2, 1, 'Medication B', '100mg', 'Take twice daily', 'dispensed'),
(3, 3, 1, 'Medication C', '75mg', 'Take once daily', 'cancelled');
