USE weight_loss_clinic;

-- Insert users
INSERT INTO users (email, password_hash, user_type) VALUES
('jane.doe@example.com', '$2b$12$gNhYhBS1n66b3YrhFD94neI5AlOiw98vi.S7TCS.5HB8.0cCoAtyy', 'patient'),
('dr.house@example.com', '$2b$12$mJcqyCWMyyj7I9xiSz8cHO66SlD6ByAx/6Xnudg0f8KZH3JwyNbke', 'doctor'),
('goodhealthrx@example.com', '$2b$12$QKo92f1qMctTcsL3qXzWh.N.j2pX0ObB71vtKCDZux0F1rFli3uCO', 'pharmacy'),
('citymeds@example.com',    '$2b$12$QKo92f1qMctTcsL3qXzWh.N.j2pX0ObB71vtKCDZux0F1rFli3uCO', 'pharmacy'),
('neighborhoodpharm@example.com', '$2b$12$QKo92f1qMctTcsL3qXzWh.N.j2pX0ObB71vtKCDZux0F1rFli3uCO', 'pharmacy'),
('dr.dahmer@example.com', '$2b$12$PU2bIEsqAbSRYpsaUmt1LelQDOQZqMgxAmkR9B81PCH5Ra2dubbhy', 'doctor'),
('dr.freeman@example.com',  '$2b$12$zvxJm/HBicsnZDP1Zfstiu0UGz7H679c0CgyHK/lZGtkuKCezJewW', 'doctor'),
('dr.brown@example.com', '$2b$12$SgQR2JV3iLekKSQ8QO8AeOlgDW3OYDX2FL4RkgOiduKrkFYP/j7Sq', 'doctor'),
('emily.stevens@example.com', '$2b$12$I3QXfmI5V7tJmBZZwyzz3uGNxs8FYY85tr2l6rbRgqw2qoy0Z2dAu', 'patient'),
('michael.brown@example.com', '$2b$12$jj0HhVkr90wtnlypNJoM3ufczq6XsuepEbH28YcMEO5VGwcwVBri.', 'patient'),
('sophia.johnson@example.com', '$2b$12$4b.19eBeIj2xWdMA06sJyecuO8WNd88D8qRIZkON0/ihQkR3T1djm', 'patient');

-- Insert patient
INSERT INTO patients (user_id, first_name, last_name, address, phone_number, zip_code) VALUES
(1, 'Jane', 'Doe', '123 Elm Street', '555-1234', '10001'),
(9, 'Emily',   'Stevens',  '400 Elm Street',    '555-0104', '10002'),
(10, 'Michael', 'Brown',     '500 Oak Avenue',    '555-0105', '10002'),
(11, 'Sophia',  'Johnson',   '600 Pine Boulevard','555-0106', '10002');

-- Insert doctor
INSERT INTO doctors (user_id, license_number, first_name, last_name, address, phone_number, ssn, description) VALUES
(2, 'DOC123456', 'Gregory', 'House', '456 Oak Avenue', '555-5678', '123-45-6789', 'Extremely mean but gets results done. There has never been any deaths under him and he is worth trusting your life with if you don’t mind your emotions being hurt.'),
(6, 'DOC222333', 'Jeffery',  'Dahmer', '234 Birch Lane',   '555-3456', '234-56-7890', 'Mostly good reviews with him. However, patients have been known to have parts of them missing after he is done treating them. Regardless, you’ll still be fine.... probably...'),
(7, 'DOC444555', 'Morgan', 'Freeman',   '345 Maple Street', '555-4567', '345-67-8901', 'Very good doctor and has a very relaxing voice. If you’re nervous, he will calm your nerves down for sure. Honestly should be a voice actor but he’s a qualified doctor instead.'),
(8, 'DOC777888', 'Emily', 'Brown', '678 Cedar Avenue', '555-7777', '987-65-4321', 'Experienced family physician specializing in internal medicine.');


-- Insert pharmacy
INSERT INTO pharmacies (user_id, name, address, zip_code, phone_number, license_number) VALUES
(3, 'GoodHealth Pharmacy', '789 Pine Road', '10002', '555-9012', 'PHARM99999'),
(4, 'CityMeds Pharmacy', '101 Main Street', '10010', '555-2222', 'PHARM10010'),
(5, 'Neighborhood Pharmacy', '202 Oak Boulevard', '07001', '555-3333', 'PHARM07001');


-- Inset Patient Meal Plan
INSERT INTO patient_meal_plans 
(patient_id, title, description, image, instructions, calories, fat, sugar, ingredients)
VALUES
(1, 'Migas', 'Traditional Mexican scrambled eggs with crispy tortillas.', 'images/migas.jpg', 'Toast the tortillas. Scramble eggs with tortillas until cooked. Serve hot.', 350, 18, 2, 'Eggs, Tortillas, Cheese, Salsa'),

(1, 'Chicken & Halloumi Burgers', 'Quick and easy grilled chicken and halloumi burgers.', 'images/burgers.jpg', 'Grill chicken and halloumi slices. Assemble into burger buns with toppings.', 550, 22, 5, 'Chicken Breast, Halloumi Cheese, Burger Buns, Lettuce, Tomato'),

(1, 'Strawberries Romanoff', 'Classic strawberries in cream dessert.', 'images/Romanoff.jpg', 'Mix strawberries with sugar and orange liqueur. Fold into whipped cream.', 320, 15, 18, 'Strawberries, Whipped Cream, Sugar, Orange Liqueur'),

(1, 'Pilaf', 'Flavored rice cooked with spices and broth.', 'images/pilaf.jpg', 'Saute onions and rice, add broth and spices. Simmer until cooked.', 400, 12, 3, 'Rice, Onion, Garlic, Broth, Spices');

-- Inset Doctor Meal Plan
INSERT INTO official_meal_plans 
(doctor_id, title, description, image, instructions, calories, fat, sugar, ingredients)
VALUES

(1, 'Potato Salad (Olivier Salad)', 'Traditional Russian potato salad with vegetables and mayonnaise.', 'images/potatoSalad.jpg', 'Boil potatoes and eggs. Dice with vegetables and mix with mayonnaise.', 450, 18, 5, 'Potatoes, Carrots, Peas, Pickles, Eggs, Mayonnaise'),

(1, 'Fish Soup (Ukha)', 'Clear Russian fish soup with light vegetables.', 'images/fishSoup.jpg', 'Simmer fish with vegetables like carrots and onions. Season and serve hot.', 280, 8, 2, 'White Fish, Carrots, Onion, Bay Leaves, Dill'),

(1, 'Beetroot Soup (Borscht)', 'Hearty beetroot soup rich in vegetables.', 'images/beetSoup.jpg', 'Cook beets, cabbage, carrots, and potatoes in broth. Add vinegar and season.', 320, 10, 7, 'Beets, Cabbage, Carrots, Potatoes, Broth, Vinegar'),

(2, 'Crock Pot Chicken Baked Tacos', 'Slow-cooked chicken tacos baked with cheese.', 'images/tacos.jpg', 'Cook chicken in crock pot with seasoning. Shred and bake in taco shells.', 500, 20, 4, 'Chicken, Taco Shells, Cheese, Taco Seasoning, Salsa'),

(2, 'Chicken Congee', 'Comforting rice porridge with shredded chicken.', 'images/congee.jpg', 'Simmer rice in broth until soft. Stir in cooked chicken.', 350, 8, 1, 'Rice, Chicken, Ginger, Broth, Green Onion'),

(2, 'Jamaican Beef Patties', 'Spiced beef filled pastries.', 'images/beefPatties.jpg', 'Prepare spiced beef filling. Fill pastry shells and bake until golden.', 420, 22, 2, 'Ground Beef, Curry Powder, Pastry Dough, Onion, Scotch Bonnet Pepper'),

(3, 'Home-made Mandazi', 'East African fried dough treat.', 'images/mandazi.jpg', 'Mix flour, coconut milk, and spices. Fry small dough pieces until golden.', 380, 15, 12, 'Flour, Coconut Milk, Sugar, Baking Powder, Cardamom'),

(3, 'Pilchard Puttanesca', 'Pasta with sardines and a spicy tomato sauce.', 'images/puttanesca.jpg', 'Cook pasta. Prepare sauce with tomatoes, sardines, olives, and capers.', 490, 16, 5, 'Pasta, Sardines, Tomatoes, Capers, Olives'),

(3, 'Blini Pancakes', 'Light Russian-style pancakes.', 'images/pancakes.jpg', 'Prepare a thin pancake batter. Cook on a skillet until golden on both sides.', 300, 10, 4, 'Flour, Milk, Eggs, Yeast, Sugar');

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
INSERT INTO payments_pharmacy (pharmacy_id, patient_id, amount, is_fulfilled, payment_date) VALUES
-- matches Orlistat price 50.00
(1, 1, 50.00, TRUE, NOW() - INTERVAL 4 DAY),
-- matches Phentermine price 45.00
(1, 1, 45.00, TRUE, NOW() - INTERVAL 3 DAY),
-- matches Lorcaserin price 55.00
(1, 1, 55.00, TRUE, NOW() - INTERVAL 2 DAY),
-- matches Liraglutide price 150.00
(1, 1, 150.00, FALSE, NOW());

INSERT INTO patient_preferred_pharmacy (patient_id, pharmacy_id) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1);

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

-- ------------------------------------
-- Initialize demo prices for all 5 drugs at each pharmacy
-- ------------------------------------
INSERT INTO pharmacy_drug_prices (pharmacy_id, drug_id, price) VALUES
  -- GoodHealth Pharmacy (pharmacy_id = 1)
  (1, 1, 50.00),   -- Orlistat
  (1, 2, 45.00),   -- Phentermine
  (1, 3, 55.00),   -- Lorcaserin
  (1, 4,150.00),   -- Liraglutide
  (1, 5,200.00),   -- Semaglutide

  -- CityMeds Pharmacy (pharmacy_id = 2)
  (2, 1, 52.00),
  (2, 2, 47.00),
  (2, 3, 57.00),
  (2, 4,155.00),
  (2, 5,205.00),

  -- Neighborhood Pharmacy (pharmacy_id = 3)
  (3, 1, 49.50),
  (3, 2, 44.00),
  (3, 3, 59.00),
  (3, 4,152.00),
  (3, 5,202.00);

-- Give Patients patientID=2,3,4 a pending prescription at GoodHealth Pharmacy
INSERT INTO prescriptions
  (doctor_id, patient_id, pharmacy_id, drug_id, dosage, instructions, status, created_at)
VALUES
  -- Emily Stevens → Orlistat
  (1, 2,     1, 1, '120mg once daily',   'Demo order', 'pending', NOW() - INTERVAL 36 HOUR),
  -- Michael Brown → Phentermine
  (1, 3,   1, 2, '37.5mg once daily',  'Demo order', 'pending', NOW() - INTERVAL 1 DAY),
  -- Sophia Johnson → Lorcaserin
  (1, 4,   1, 3, '10mg twice daily',   'Demo order', 'pending', NOW() - INTERVAL 12 HOUR),
  -- Jane Doe Prescription History
  -- 4 days ago: Orlistat
  (1, 1, 1, 1, '120mg once daily', 'Dispensed script 1', 'dispensed', NOW() - INTERVAL 4 DAY),
  -- 3 days ago: Phentermine
  (1, 1, 1, 2, '37.5mg once daily', 'Dispensed script 2', 'dispensed', NOW() - INTERVAL 3 DAY),
  -- 2 days ago: Lorcaserin
  (1, 1, 1, 3, '10mg twice daily', 'Dispensed script 3', 'dispensed', NOW() - INTERVAL 2 DAY),
  -- 1 day ago: Liraglutide (still pending)
  (1, 1, 1, 4, '1.8mg daily',    'Pending script',     'pending',   NOW());

INSERT INTO discussion_board (post_id, doctor_id, post_title, post_content, created_at) VALUES
(1, 3, 'Buckwheat Kasha', 
 '{"fat": 3, "image": "images/buckwheat.jpg", "sugar": 0, "calories": 150, "description": "Classic Eastern European porridge made from buckwheat.", "ingredients": "Buckwheat, Water, Salt, Butter", "instructions": "Boil buckwheat in salted water until soft. Add butter and serve."}', 
 '2025-05-01 10:15:43'),

(2, 1, 'Stuffed Peppers', 
 '{"fat": 12, "image": "images/stuffedPeppers.jpg", "sugar": 6, "calories": 320, "description": "Bell peppers filled with a mix of rice and meat, cooked in tomato sauce.", "ingredients": "Bell Peppers, Ground Beef, Rice, Onion, Tomato Sauce", "instructions": "Mix beef with rice and onion. Stuff into peppers. Simmer in tomato sauce until cooked through."}', 
 '2025-05-01 10:18:22'),

(3, 1, 'Cabbage Rolls (Golubtsy)', 
 '{"fat": 10, "image": "images/cabbageRolls.jpg", "sugar": 4, "calories": 350, "description": "Cabbage leaves filled with meat and rice, simmered in tomato sauce.", "ingredients": "Cabbage Leaves, Ground Meat, Rice, Onion, Tomato Sauce", "instructions": "Wrap meat and rice mixture in cabbage leaves. Cook in tomato sauce until tender."}', 
 '2025-05-01 10:20:55'),

(4, 2, 'Oatmeal with Berries', 
 '{"fat": 5, "image": "images/oatmealBerries.jpg", "sugar": 10, "calories": 220, "description": "Healthy breakfast oats topped with mixed berries.", "ingredients": "Oats, Milk or Water, Strawberries, Blueberries, Honey", "instructions": "Cook oats with liquid. Top with berries and drizzle honey."}', 
 '2025-05-01 10:25:10'),
(5, 4, 'Chicken Kotleti', 
 '{"fat": 15, "image": "images/chickenKotleti.jpg", "sugar": 1, "calories": 310, "description": "Pan-fried chicken patties with herbs and onion.", "ingredients": "Ground Chicken, Onion, Egg, Bread Crumbs, Spices", "instructions": "Mix all ingredients, form patties, and pan-fry until golden."}', 
 '2025-05-01 10:28:47');