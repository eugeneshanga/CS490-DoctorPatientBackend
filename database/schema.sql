-- Create the database
CREATE DATABASE IF NOT EXISTS weight_loss_clinic;
USE weight_loss_clinic;

-- Users table (abstraction for all user types)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type ENUM('patient', 'doctor', 'pharmacy') NOT NULL
);

-- Patients table
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address TEXT,
    phone_number VARCHAR(20),
    zip_code VARCHAR(5),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Doctors table
CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address TEXT,
    phone_number VARCHAR(20),
    ssn VARCHAR(11) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Pharmacies table (handles login via users table)
CREATE TABLE pharmacies (
    pharmacy_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    zip_code VARCHAR(5),
    phone_number VARCHAR(20) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Medical Metrics table
CREATE TABLE medical_metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    caloric_intake INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- Doctor-Patient Relationship
CREATE TABLE doctor_patient (
    doctor_id INT,
    patient_id INT,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (doctor_id, patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- Appointments table
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    appointment_time DATETIME NOT NULL,
    status ENUM('scheduled', 'accepted', 'rejected', 'completed', 'canceled') NOT NULL DEFAULT 'scheduled',
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

CREATE TABLE chat_history (
  chat_id        INT NOT NULL AUTO_INCREMENT,
  patient_id     INT NOT NULL,
  doctor_id      INT NOT NULL,
  appointment_id INT NOT NULL,
  sender_type    ENUM('doctor','patient') NOT NULL,
  message        TEXT NOT NULL,
  sent_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (chat_id),

  -- lookups by appointment
  KEY idx_chat_appointment (appointment_id),
  -- optional composite lookup if you query by doctor+patient frequently
  KEY idx_chat_doc_pat        (doctor_id, patient_id),

  -- foreign keys
  CONSTRAINT fk_chat_patient     FOREIGN KEY (patient_id)     REFERENCES patients(patient_id)     ON DELETE CASCADE,
  CONSTRAINT fk_chat_doctor      FOREIGN KEY (doctor_id)      REFERENCES doctors(doctor_id)      ON DELETE CASCADE,
  CONSTRAINT fk_chat_appointment FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4;


-- Payments table (Patient to Doctor)
CREATE TABLE payments_doctor (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    is_fulfilled BOOLEAN DEFAULT FALSE,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- Payments table (Patient to Pharmacy)
CREATE TABLE payments_pharmacy (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    pharmacy_id INT NOT NULL,
    patient_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    is_fulfilled BOOLEAN DEFAULT FALSE,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(pharmacy_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- Patient Meal Plans: These are private meal plans for patients.
CREATE TABLE patient_meal_plans (
    meal_plan_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image LONGBLOB,
    instructions TEXT,
    calories INT,
    fat INT,
    sugar INT,
    ingredients TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- Pharmacy Inventory Table
CREATE TABLE pharmacy_inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    pharmacy_id INT NOT NULL,
    drug_name VARCHAR(100) NOT NULL,
    stock_quantity INT NOT NULL,
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(pharmacy_id) ON DELETE CASCADE
);

-- Discussion Board (Meal Plans by Doctors)
CREATE TABLE discussion_board (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    post_title VARCHAR(255) NOT NULL,
    post_content JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

-- Replies to Discussion Board posts
CREATE TABLE post_replies (
    reply_id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    patient_id INT NOT NULL,
    reply_content TEXT NOT NULL,
    replied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES discussion_board(post_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- Ratings table
CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_id INT NOT NULL,
    rating DECIMAL(2,1) CHECK (rating BETWEEN 0.0 AND 5.0),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    UNIQUE (patient_id, doctor_id, appointment_id)
);

-- Aggregated Doctor Ratings table
CREATE TABLE doctor_ratings (
    doctor_id INT PRIMARY KEY,
    total_ratings INT DEFAULT 0,
    average_rating FLOAT DEFAULT 0,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

-- Prescriptions table
CREATE TABLE prescriptions (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    pharmacy_id INT NULL,
    medication_name VARCHAR(255) NOT NULL,
    dosage VARCHAR(255) NOT NULL,
    instructions TEXT NOT NULL,
    status ENUM('pending', 'dispensed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(pharmacy_id) ON DELETE SET NULL
);

CREATE TABLE official_meal_plans (
    meal_plan_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image LONGBLOB,
    instructions TEXT,
    calories INT,
    fat INT,
    sugar INT,
    ingredients TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

-- Mapping Table: To assign a doctor's official meal plan to multiple patients.
CREATE TABLE patient_assigned_meal_plans (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    meal_plan_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (meal_plan_id) REFERENCES official_meal_plans(meal_plan_id) ON DELETE CASCADE,
    UNIQUE (patient_id, meal_plan_id)
);

-- Doctor transaction payment details
CREATE TABLE doctor_payment_details (
  detail_id        INT AUTO_INCREMENT PRIMARY KEY,
  payment_id       INT            NOT NULL,
  cardholder_name  VARCHAR(255)   NOT NULL,
  card_number      VARCHAR(20)    NOT NULL,
  exp_month        TINYINT UNSIGNED NOT NULL,  -- 1–12
  exp_year         SMALLINT UNSIGNED NOT NULL, -- full year, e.g. 2025
  cvv              VARCHAR(4)     NOT NULL,
  created_at       TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_doc_pay
    FOREIGN KEY (payment_id)
    REFERENCES payments_doctor(payment_id)
    ON DELETE CASCADE
);


-- Pharmacy transaction payment details
CREATE TABLE pharmacy_payment_details (
  detail_id        INT AUTO_INCREMENT PRIMARY KEY,
  payment_id       INT            NOT NULL,
  cardholder_name  VARCHAR(255)   NOT NULL,
  card_number      VARCHAR(20)    NOT NULL,
  exp_month        TINYINT UNSIGNED NOT NULL,  -- 1–12
  exp_year         SMALLINT UNSIGNED NOT NULL, -- full year, e.g. 2025
  cvv              VARCHAR(4)     NOT NULL,
  created_at       TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_pharm_pay
    FOREIGN KEY (payment_id)
    REFERENCES payments_pharmacy(payment_id)
    ON DELETE CASCADE
);
