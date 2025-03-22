from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG
from mysql.connector import Error


registration_bp = Blueprint('registration', __name__)


# ------------------------------------
# Patient Registration Endpoint
# ------------------------------------
@registration_bp.route('/api/register/patient', methods=['POST'])
def register_patient():
    data = request.get_json()

    # Extract fields from the incoming JSON
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

    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Insert the new patient record into the database.
        query = (
            "INSERT INTO patients "
            "(email, password_hash, first_name, last_name, "
            "address, phone_number, zip_code)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        values = (email, password, first_name,
                  last_name, address, phone_number, zip_code)
        cursor.execute(query, values)
        connection.commit()

        return jsonify({"message": "Patient registered successfully"}), 201

    except Error as err:
        print("Database error:", err)
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

    # Extract fields from the incoming JSON
    email = data.get('email')
    password = data.get('password')
    license_number = data.get('license_number')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    address = data.get('address')
    phone_number = data.get('phone_number')
    ssn = data.get('ssn')

    # Validate required fields
    if not email or not password or not license_number:
        if not first_name or not last_name or not ssn:
            return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = (
            "INSERT INTO doctors "
            "(email, password_hash, license_number, "
            "first_name, last_name, address, phone_number, ssn)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        values = (email, password, license_number, first_name, last_name, address, phone_number, ssn)
        cursor.execute(query, values)
        connection.commit()

        return jsonify({"message": "Doctor registered successfully"}), 201

    except Error as err:
        print("Database error:", err)
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

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Step 1: Insert into users table
        insert_user = (
            "INSERT INTO users (email, password_hash, user_type) "
            "VALUES (%s, %s, 'pharmacy')"
        )
        cursor.execute(insert_user, (email, password))
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

    except Error as err:
        print("Database error:", err)
        connection.rollback()
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
