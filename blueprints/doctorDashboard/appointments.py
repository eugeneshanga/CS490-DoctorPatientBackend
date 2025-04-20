from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

doctor_dashboard_appointments_bp = Blueprint('doctor_dashboard_appointments', __name__, url_prefix='/api/doctor-dashboard/appointments')


@doctor_dashboard_appointments_bp.route('/', methods=['GET'])
def get_scheduled_appointments():
    """
    Endpoint to fetch all scheduled (pending) appointments for a doctor.
    Expects a query parameter 'user_id' representing the doctor's user ID.
    Converts user_id to doctor_id, then retrieves all appointments with status 'scheduled'.

    Returns:
      A JSON array of appointments with fields:
        - appointment_id
        - patient_id
        - appointment_time
        - status
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to doctor_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        if not doctor:
            return jsonify({"error": "Doctor not found for given user_id"}), 404
        doctor_id = doctor["doctor_id"]

        # Query appointments with status 'scheduled'
        sql = """
            SELECT appointment_id, patient_id, appointment_time, status
            FROM appointments
            WHERE doctor_id = %s AND status = 'scheduled'
            ORDER BY appointment_time ASC
        """
        cursor.execute(sql, (doctor_id,))
        appointments = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(appointments), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@doctor_dashboard_appointments_bp.route('/respond', methods=['POST'])
def respond_to_appointment():
    """
    Endpoint for a doctor to respond to an appointment request.
    Expects JSON with:
      - user_id: The doctor's user ID.
      - appointment_id: The ID of the appointment to respond to.
      - accepted: A binary value (true/false) indicating whether the appointment is accepted.

    The appointment's status is updated to "accepted" if accepted is true,
    or "rejected" if accepted is false.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    appointment_id = data.get('appointment_id')
    accepted = data.get('accepted')  # Expecting a boolean

    if user_id is None or appointment_id is None or accepted is None:
        return jsonify({"error": "Missing required fields: user_id, appointment_id, accepted"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to doctor_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        if not doctor:
            return jsonify({"error": "Doctor not found for given user_id"}), 404
        doctor_id = doctor["doctor_id"]

        # Verify that the appointment belongs to this doctor
        cursor.execute("SELECT * FROM appointments WHERE appointment_id = %s AND doctor_id = %s",
                       (appointment_id, doctor_id))
        appointment = cursor.fetchone()
        if not appointment:
            return jsonify({"error": "Appointment not found or does not belong to this doctor"}), 404

        # Determine the new status based on the accepted value
        new_status = "accepted" if accepted else "rejected"

        # Update the appointment's status
        update_sql = "UPDATE appointments SET status = %s WHERE appointment_id = %s"
        cursor.execute(update_sql, (new_status, appointment_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": f"Appointment has been {new_status}"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@doctor_dashboard_appointments_bp.route('/accepted', methods=['GET'])
def get_accepted_appointments():
    """
    Endpoint to fetch all accepted appointments for a doctor.
    Expects a query parameter 'user_id' representing the doctor's user ID.
    Converts user_id to doctor_id, then retrieves all appointments with status 'accepted'.

    Returns a JSON array of appointments with fields:
      - appointment_id
      - patient_id
      - appointment_time
      - status
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to doctor_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        if not doctor:
            return jsonify({"error": "Doctor not found for given user_id"}), 404
        doctor_id = doctor["doctor_id"]

        # Retrieve appointments with status 'accepted'
        sql = """
            SELECT appointment_id, patient_id, appointment_time, status
            FROM appointments
            WHERE doctor_id = %s AND status = 'accepted'
            ORDER BY appointment_time ASC
        """
        cursor.execute(sql, (doctor_id,))
        appointments = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(appointments), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@doctor_dashboard_appointments_bp.route('/canceled', methods=['GET'])
def get_canceled_appointments():
    """
    Endpoint to fetch all canceled appointments for a doctor.
    Expects a query parameter 'user_id' representing the doctor's user ID.
    Converts user_id to doctor_id, then retrieves all appointments with status 'canceled'.

    Returns a JSON array of appointments with fields:
      - appointment_id
      - patient_id
      - appointment_time
      - status
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to doctor_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        if not doctor:
            return jsonify({"error": "Doctor not found for given user_id"}), 404
        doctor_id = doctor["doctor_id"]

        # Retrieve appointments with status 'canceled'
        sql = """
            SELECT appointment_id, patient_id, appointment_time, status
            FROM appointments
            WHERE doctor_id = %s AND status = 'canceled'
            ORDER BY appointment_time ASC
        """
        cursor.execute(sql, (doctor_id,))
        appointments = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(appointments), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@doctor_dashboard_appointments_bp.route('/completed', methods=['GET'])
def get_completed_appointments():
    """
    Endpoint to fetch all completed appointments for a doctor.
    Expects a query parameter 'user_id' representing the doctor's user ID.
    Converts user_id to doctor_id, then retrieves all appointments with status 'completed'.

    Returns a JSON array of appointments with fields:
      - appointment_id
      - patient_id
      - appointment_time
      - status
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to doctor_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        if not doctor:
            return jsonify({"error": "Doctor not found for given user_id"}), 404
        doctor_id = doctor["doctor_id"]

        # Retrieve appointments with status 'completed'
        sql = """
            SELECT appointment_id, patient_id, appointment_time, status
            FROM appointments
            WHERE doctor_id = %s AND status = 'completed'
            ORDER BY appointment_time ASC
        """
        cursor.execute(sql, (doctor_id,))
        appointments = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(appointments), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@doctor_dashboard_appointments_bp.route('/complete', methods=['PATCH'])
def complete_appointment():
    data = request.get_json()
    appt_id = data.get('appointment_id')
    if not appt_id:
        return jsonify({"error": "Missing appointment_id"}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE appointments
               SET status='completed'
             WHERE appointment_id = %s
        """, (appt_id,))
        conn.commit()
        return jsonify({"message": "Appointment completed"}), 200

    except Exception as e:
        print("❌ Error completing appointment:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
