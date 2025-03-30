from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

patient_dashboard_bp = Blueprint('patient_dashboard', __name__, url_prefix='/api/patient-dashboard')


@patient_dashboard_bp.route('/search-doctors', methods=['GET'])
def search_doctors():
    """
    Endpoint to search for doctors based on a query.
    Returns only the necessary fields: doctor_id, first_name, last_name,
    license_number, and phone_number.
    """
    search_query = request.args.get('query', default='', type=str)

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        if search_query:
            # Use a LIKE query to match the first or last name
            like_query = f"%{search_query}%"
            sql = """
                SELECT doctor_id, first_name, last_name, license_number, phone_number
                FROM doctors
                WHERE is_active = TRUE AND (first_name LIKE %s OR last_name LIKE %s)
            """
            cursor.execute(sql, (like_query, like_query))
        else:
            # If no search term, return all active doctors with selected fields
            sql = """
                SELECT doctor_id, first_name, last_name, license_number, phone_number
                FROM doctors
                WHERE is_active = TRUE
            """
            cursor.execute(sql)

        doctors = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(doctors), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@patient_dashboard_bp.route('/meal-plans', methods=['GET'])
def get_meal_plans():
    """
    Endpoint to fetch all meal plans for a given patient.
    Expects a query parameter `patient_id` to identify the logged in patient.
    Returns a list of meal plans.
    """
    patient_id = request.args.get('patient_id', type=int)

    if not patient_id:
        return jsonify({"error": "patient_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Retrieve all meal plans for the patient, ordered by creation date descending
        sql = """
            SELECT meal_plan_id, patient_id, meal_plan, created_at
            FROM patient_meal_plans
            WHERE patient_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (patient_id,))
        meal_plans = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(meal_plans), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@patient_dashboard_bp.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    """
    Endpoint to fetch all prescriptions for a given patient.
    Expects a query parameter `patient_id` identifying the logged-in patient.
    Returns a list of prescriptions.
    """
    patient_id = request.args.get('patient_id', type=int)

    if not patient_id:
        return jsonify({"error": "patient_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        sql = """
            SELECT prescription_id, doctor_id, patient_id, pharmacy_id, medication_name,
                   dosage, instructions, status, created_at
            FROM prescriptions
            WHERE patient_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (patient_id,))
        prescriptions = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(prescriptions), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
