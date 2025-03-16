
-- Use the correct database
USE weight_loss_clinic;

-- Insert test data for patients
INSERT INTO patients (email, password_hash, first_name, last_name, address, phone_number, zip_code, is_active)
VALUES
('patient1@example.com', 'hashed_password1', 'John', 'Doe', '123 Maple St', '555-1234', '10001', TRUE),
('patient2@example.com', 'hashed_password2', 'Jane', 'Smith', '456 Oak St', '555-5678', '10002', TRUE),
('patient3@example.com', 'hashed_password3', 'Alice', 'Johnson', '789 Pine St', '555-8765', '10003', TRUE);

-- Insert test data for medical metrics
INSERT INTO medical_metrics (patient_id, weight, height, caloric_intake)
VALUES
(1, 75.5, 1.75, 2000),
(2, 68.0, 1.68, 1800),
(3, 82.3, 1.80, 2200);

-- Insert test data for doctors
INSERT INTO doctors (email, password_hash, license_number, first_name, last_name, address, phone_number, ssn, is_active)
VALUES
('doctor1@example.com', 'hashed_password4', 'DOC123456', 'Dr. Mark', 'Brown', '12 Med Street', '555-9999', '123-45-6789', TRUE),
('doctor2@example.com', 'hashed_password5', 'DOC654321', 'Dr. Susan', 'Davis', '34 Health Ave', '555-8888', '987-65-4321', TRUE);

-- Insert test data for doctor-patient relationships
INSERT INTO doctor_patient (doctor_id, patient_id)
VALUES
(1, 1),
(1, 2),
(2, 3);

-- Insert test data for appointments
INSERT INTO appointments (doctor_id, patient_id, appointment_time, status)
VALUES
(1, 1, '2025-03-20 10:00:00', 'scheduled'),
(1, 2, '2025-03-21 14:00:00', 'scheduled'),
(2, 3, '2025-03-22 16:30:00', 'scheduled');

-- Insert test data for chat history
INSERT INTO chat_history (patient_id, doctor_id, message, sent_at)
VALUES
(1, 1, 'Hello Doctor, I have a question about my diet.', NOW()),
(2, 1, 'I need a follow-up on my recent test results.', NOW()),
(3, 2, 'How can I improve my weight loss progress?', NOW());

-- Insert test data for payments (Doctor)
INSERT INTO payments_doctor (doctor_id, patient_id, amount, is_fulfilled)
VALUES
(1, 1, 100.00, TRUE),
(1, 2, 120.50, FALSE),
(2, 3, 90.75, TRUE);

-- Insert test data for pharmacies
INSERT INTO pharmacies (name, address, zip_code, phone_number, license_number, is_active)
VALUES
('Wellness Pharmacy', '101 Main St', '20001', '555-4321', 'PHARM001', TRUE),
('HealthFirst Pharmacy', '202 Broadway', '20002', '555-8765', 'PHARM002', TRUE);

-- Insert test data for pharmacy admins
INSERT INTO pharmacy_admins (pharmacy_id, email, password_hash, first_name, last_name, phone_number, is_active)
VALUES
(1, 'admin1@pharmacy.com', 'hashed_password6', 'Mike', 'Adams', '555-1111', TRUE),
(1, 'admin2@pharmacy.com', 'hashed_password7', 'Sarah', 'Clark', '555-2222', TRUE),
(2, 'admin3@pharmacy.com', 'hashed_password8', 'Daniel', 'Green', '555-3333', TRUE);

-- Insert test data for payments (Pharmacy)
INSERT INTO payments_pharmacy (pharmacy_id, patient_id, amount, is_fulfilled)
VALUES
(1, 1, 50.00, TRUE),
(2, 2, 75.25, FALSE),
(1, 3, 60.50, TRUE);

-- Insert test data for patient meal plans
INSERT INTO patient_meal_plans (patient_id, meal_plan)
VALUES
(1, '{"breakfast": "Oatmeal", "lunch": "Grilled Chicken Salad", "dinner": "Steamed Fish"}'),
(2, '{"breakfast": "Scrambled Eggs", "lunch": "Quinoa Bowl", "dinner": "Vegetable Stir-fry"}'),
(3, '{"breakfast": "Smoothie", "lunch": "Turkey Sandwich", "dinner": "Grilled Salmon"}');

-- Insert test data for pharmacy inventory
INSERT INTO pharmacy_inventory (pharmacy_id, drug_name, stock_quantity)
VALUES
(1, 'Weight Loss Supplement A', 100),
(1, 'Protein Powder B', 50),
(2, 'Fat Burner C', 75);

-- Insert test data for discussion board
INSERT INTO discussion_board (doctor_id, post_title, post_content)
VALUES
(1, 'Effective Meal Plans for Weight Loss', '{"text": "Here are some meal plans I recommend for weight loss...", "tips": ["Reduce sugar", "Eat more protein"]}'),
(2, 'Workout and Nutrition Balance', '{"text": "How to balance workouts and nutrition for effective weight loss..."}');
