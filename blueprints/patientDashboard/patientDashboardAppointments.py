from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

patient_dashboard_appointments_bp = Blueprint('patient_dashboard_appointments', __name__, url_prefix='/api/patient-dashboard/appointments')


@patient_dashboard_appointments_bp.route('/', methods=['GET'])
def get_appointments():
    """
    Endpoint to fetch current (upcoming) and previous (past) appointments for a given patient.
    Now expects a query parameter `user_id` and converts it to a patient_id.
    Returns a JSON object with two keys: "upcoming" and "past".
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to patient_id
        cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found for given user_id"}), 404
        patient_id = patient["patient_id"]

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


@patient_dashboard_appointments_bp.route('/patient_appointment', methods=['POST'])
def patient_appointment():
    """
    Endpoint for a patient to request an appointment.
    Expects JSON with:
      - user_id: The ID of the user (patient)
      - doctor_id: The ID of the doctor the patient wants an appointment with
      - appointment_time: The desired appointment datetime (e.g., "2025-04-15 14:30:00")
    """

    data = request.get_json()
    user_id = data.get('user_id')
    doctor_id = data.get('doctor_id')
    appointment_time = data.get('appointment_time')

    if not user_id or not doctor_id or not appointment_time:
        return jsonify({"error": "Missing required fields: user_id, doctor_id, appointment_time"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to patient_id
        cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found for given user_id"}), 404
        patient_id = patient["patient_id"]

        # Insert a new appointment with a 'scheduled' status
        # Here, 'scheduled' is used to mean "pending confirmation" until the doctor updates it.
        sql = """
            INSERT INTO appointments (doctor_id, patient_id, appointment_time, status)
            VALUES (%s, %s, %s, 'scheduled')
        """
        cursor.execute(sql, (doctor_id, patient_id, appointment_time))
        connection.commit()
        appointment_id = cursor.lastrowid

        cursor.close()
        connection.close()
        return jsonify({"message": "Appointment request submitted", "appointment_id": appointment_id}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@patient_dashboard_appointments_bp.route('/cancel_appointment', methods=['PATCH'])
def cancel_appointment():
    """
    Endpoint for a patient to cancel an appointment.
    Expects JSON with:
      - user_id: The ID of the user (patient)
      - appointment_id: The ID of the appointment to cancel.

    Only the owner of the appointment can cancel it.
    The appointment's status is updated to 'canceled'.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    appointment_id = data.get('appointment_id')

    if not user_id or not appointment_id:
        return jsonify({"error": "Missing required fields: user_id, appointment_id"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to patient_id
        cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found for given user_id"}), 404
        patient_id = patient["patient_id"]

        # Verify that the appointment belongs to this patient
        cursor.execute(
            "SELECT * FROM appointments WHERE appointment_id = %s AND patient_id = %s",
            (appointment_id, patient_id)
        )
        appointment = cursor.fetchone()
        if not appointment:
            return jsonify({"error": "Appointment not found for given appointment_id and patient"}), 404

        # Update the appointment status to 'canceled'
        update_sql = "UPDATE appointments SET status = 'canceled' WHERE appointment_id = %s"
        cursor.execute(update_sql, (appointment_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Appointment canceled successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
