from flask import Blueprint, request, jsonify
import mysql.connector
import bcrypt
from config import DB_CONFIG

registration_bp = Blueprint('registration', __name__)


# ------------------------------------
# Patient Registration Endpoint
# ------------------------------------
@registration_bp.route('/api/register/patient', methods=['POST'])
def register_patient():
    data = request.get_json()

    # Extract fields
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    address = data.get('address')
    phone_number = data.get('phone_number')
    zip_code = data.get('zip_code')

    # Validate required fields
    if not email or not password or not first_name or not last_name:
        return jsonify({"error": "Missing required fields"}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Step 1: Insert into users
        insert_user = (
            "INSERT INTO users (email, password_hash, user_type) "
            "VALUES (%s, %s, 'patient')"
        )
        cursor.execute(insert_user, (email, hashed_password))
        user_id = cursor.lastrowid

        # Step 2: Insert into patients
        insert_patient = (
            "INSERT INTO patients (user_id, first_name, last_name, address, phone_number, zip_code) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        values = (user_id, first_name, last_name, address, phone_number, zip_code)
        cursor.execute(insert_patient, values)

        connection.commit()
        return jsonify({"message": "Patient registered successfully"}), 201

    except mysql.connector.Error as err:
        print("Database error:", err)
        connection.rollback()
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ------------------------------------
# Doctor Registration Endpoint
# ------------------------------------
@registration_bp.route('/api/register/doctor', methods=['POST'])
def register_doctor():
    data = request.get_json()

    # Extract fields
    email = data.get('email')
    password = data.get('password')
    license_number = data.get('license_number')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    address = data.get('address')
    phone_number = data.get('phone_number')
    ssn = data.get('ssn')

    # Validate required fields
    if not email or not password or not license_number or not first_name or not last_name or not ssn:
        return jsonify({"error": "Missing required fields"}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Step 1: Insert into users
        insert_user = (
            "INSERT INTO users (email, password_hash, user_type) "
            "VALUES (%s, %s, 'doctor')"
        )
        cursor.execute(insert_user, (email, hashed_password))
        user_id = cursor.lastrowid

        # Step 2: Insert into doctors
        insert_doctor = (
            "INSERT INTO doctors (user_id, license_number, first_name, last_name, address, phone_number, ssn) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        values = (user_id, license_number, first_name, last_name, address, phone_number, ssn)
        cursor.execute(insert_doctor, values)

        connection.commit()
        return jsonify({"message": "Doctor registered successfully"}), 201

    except mysql.connector.Error as err:
        print("Database error:", err)
        connection.rollback()
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ------------------------------------
# Pharmacy Registration Endpoint
# ------------------------------------
@registration_bp.route('/api/register/pharmacy', methods=['POST'])
def register_pharmacy():
    data = request.get_json()

    # Extract fields from the incoming JSON
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    address = data.get('address')
    zip_code = data.get('zip_code')
    phone_number = data.get('phone_number')
    license_number = data.get('license_number')

    # Validate required fields
    if not email or not password or not name or not address or not phone_number or not license_number:
        return jsonify({"error": "Missing required fields"}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Step 1: Insert into users table
        insert_user = (
            "INSERT INTO users (email, password_hash, user_type) "
            "VALUES (%s, %s, 'pharmacy')"
        )
        cursor.execute(insert_user, (email, hashed_password))
        user_id = cursor.lastrowid

        # Step 2: Insert into pharmacies table
        insert_pharmacy = (
            "INSERT INTO pharmacies (user_id, name, address, zip_code, phone_number, license_number) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        values = (user_id, name, address, zip_code, phone_number, license_number)
        cursor.execute(insert_pharmacy, values)

        connection.commit()

        return jsonify({"message": "Pharmacy registered successfully"}), 201

    except mysql.connector.Error as err:
        print("Database error:", err)
        connection.rollback()
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
