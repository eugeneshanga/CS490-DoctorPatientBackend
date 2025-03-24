from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

appointments_bp = Blueprint("appointments", __name__, url_prefix="/api/appointments")


@appointments_bp.route('/create', methods=['POST'])
def create_appointment():
    data = request.get_json()

    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    appointment_time = data.get('appointment_time')

    if not patient_id or not doctor_id or not appointment_time:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_time)
            VALUES (%s, %s, %s)
        """, (patient_id, doctor_id, appointment_time))
        connection.commit()

        return jsonify({"message": "Appointment created successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@appointments_bp.route('/confirm/<int:appointment_id>', methods=['POST'])
def confirm_appointment(appointment_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print("Confirming appointment ID:", appointment_id)

        # make sure there is apointment
        cursor.execute("SELECT appointment_id, status FROM appointments WHERE appointment_id = %s", (appointment_id,))
        appointment = cursor.fetchone()

        if not appointment:
            print("❌ Appointment not found:", appointment_id)  #wrong apopintment
            return jsonify({"error": "Appointment not found"}), 404

        print("✅ Appointment found, current status:", appointment[1])


        cursor.execute("""
            UPDATE appointments SET status = 'completed' WHERE appointment_id = %s
        """, (appointment_id,))
        connection.commit()

        return jsonify({"message": "Appointment completed"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@appointments_bp.route('/all', methods=['GET'])
def get_all_appointments():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # get all the appointment
        cursor.execute("""
            SELECT a.appointment_id, a.patient_id, a.doctor_id, u.email AS doctor_email, a.appointment_date, a.status 
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            JOIN users u ON d.user_id = u.user_id
        """)
        appointments = cursor.fetchall()

        result = []
        for row in appointments:
            result.append({
                "appointment_id": row[0],
                "patient_id": row[1],
                "doctor_id": row[2],
                "doctor_email": row[3],
                "appointment_date": row[4],
                "status": row[5]
            })

        return jsonify(result), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@appointments_bp.route('/decision/<int:appointment_id>', methods=['POST'])
def doctor_decision(appointment_id):
    data = request.get_json()
    decision = data.get('decision')  # 'accepted' or 'rejected'

    if decision not in ['accepted', 'rejected']:
        return jsonify({"error": "Invalid decision. Use 'accepted' or 'rejected'."}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print("Processing decision for appointment:", appointment_id, "Decision:", decision)

        #make sure there is appointment
        cursor.execute("SELECT appointment_id, status FROM appointments WHERE appointment_id = %s", (appointment_id,))
        appointment = cursor.fetchone()

        if not appointment:
            print("❌ Appointment not found:", appointment_id)
            return jsonify({"error": "Appointment not found"}), 404

        if appointment[1] not in ['scheduled']:
            return jsonify({"error": f"Cannot change status from '{appointment[1]}'"}), 403

        # update apointment status
        cursor.execute("""
            UPDATE appointments SET status = %s WHERE appointment_id = %s
        """, (decision, appointment_id))
        connection.commit()

        return jsonify({"message": f"Appointment {decision}"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@appointments_bp.route('/cancel/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    data = request.get_json()
    user_role = data.get('role')  # 'patient' or 'doctor'

    if user_role not in ['patient', 'doctor']:
        return jsonify({"error": "Invalid role. Use 'patient' or 'doctor'."}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print(f"User ({user_role}) is canceling appointment ID: {appointment_id}")

        # make sure there is apponitment 
        cursor.execute("SELECT appointment_id, status FROM appointments WHERE appointment_id = %s", (appointment_id,))
        appointment = cursor.fetchone()

        if not appointment:
            print("❌ Appointment not found:", appointment_id)  # wrong appointment
            return jsonify({"error": "Appointment not found"}), 404

        if appointment[1] in ['completed', 'canceled']:
            return jsonify({"error": f"Cannot cancel an appointment with status '{appointment[1]}'"}), 403

        # update to  `canceled`
        cursor.execute("""
            UPDATE appointments SET status = 'canceled' WHERE appointment_id = %s
        """, (appointment_id,))
        connection.commit()

        return jsonify({"message": f"Appointment {appointment_id} has been canceled by {user_role}"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()
