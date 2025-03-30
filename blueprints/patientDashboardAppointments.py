from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

patient_dashboard_appointments_bp = Blueprint('patient_dashboard_appointments', __name__, url_prefix='/api/patient-dashboard/appointments')


@patient_dashboard_appointments_bp.route('/', methods=['GET'])
def get_appointments():
    """
    Endpoint to fetch current (upcoming) and previous (past) appointments for a given patient.
    Expects a query parameter `patient_id`.
    Returns a JSON object with two keys: "upcoming" and "past".
    """
    patient_id = request.args.get('patient_id', type=int)
    if not patient_id:
        return jsonify({"error": "patient_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Fetch upcoming appointments (appointments that have not yet occurred)
        upcoming_sql = """
            SELECT appointment_id, doctor_id, patient_id, appointment_time, status
            FROM appointments
            WHERE patient_id = %s AND appointment_time >= NOW()
            ORDER BY appointment_time ASC
        """
        cursor.execute(upcoming_sql, (patient_id,))
        upcoming_appointments = cursor.fetchall()

        # Fetch past appointments (appointments that have already occurred)
        past_sql = """
            SELECT appointment_id, doctor_id, patient_id, appointment_time, status
            FROM appointments
            WHERE patient_id = %s AND appointment_time < NOW()
            ORDER BY appointment_time DESC
        """
        cursor.execute(past_sql, (patient_id,))
        past_appointments = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({
            "upcoming": upcoming_appointments,
            "past": past_appointments
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
