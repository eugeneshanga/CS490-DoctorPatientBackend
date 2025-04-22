from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")


# Send Chat Message
@chat_bp.route('/send', methods=['POST'])
def send_message():
    data = request.get_json() or {}
    required = ['patient_id', 'doctor_id', 'appointment_id', 'sender_type', 'message']
    missing = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify(error=f"Missing required field(s): {', '.join(missing)}"), 400

    patient_id = data['patient_id']
    doctor_id = data['doctor_id']
    appointment_id = data['appointment_id']
    sender_type = data['sender_type']
    message = data['message']

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO chat_history
              (patient_id, doctor_id, appointment_id, sender_type, message)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (patient_id, doctor_id, appointment_id, sender_type, message)
        )
        conn.commit()
        return jsonify(message="Message sent"), 201

    except mysql.connector.Error as e:
        print("❌ Error inserting message:", e)
        return jsonify(error="Internal server error"), 500

    finally:
        cursor.close()
        conn.close()


# Get Chat History For Patient Doctor Appointment
@chat_bp.route('/history', methods=['GET'])
def get_chat_history():
    patient_id = request.args.get('patient_id')
    doctor_id = request.args.get('doctor_id')
    appointment_id = request.args.get('appointment_id')

    missing = [
        p for p in ('patient_id', 'doctor_id', 'appointment_id')
        if not request.args.get(p)
    ]
    if missing:
        return jsonify(error=f"Missing query param(s): {', '.join(missing)}"), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT chat_id, patient_id, doctor_id, appointment_id,
                   sender_type, message, sent_at
              FROM chat_history
             WHERE patient_id     = %s
               AND doctor_id      = %s
               AND appointment_id = %s
             ORDER BY sent_at ASC
            """,
            (patient_id, doctor_id, appointment_id)
        )
        messages = cursor.fetchall()
        return jsonify(messages), 200

    except mysql.connector.Error as e:
        print("❌ Error loading messages:", e)
        return jsonify(error="Internal server error"), 500

    finally:
        cursor.close()
        conn.close()


# Returns
@chat_bp.route('/appointments', methods=['GET'])
def list_appointments():
    doctor_id = request.args.get('doctor_id')
    patient_id = request.args.get('patient_id')

    missing = [p for p in ('doctor_id', 'patient_id') if not request.args.get(p)]
    if missing:
        return jsonify(error=f"Missing query param(s): {', '.join(missing)}"), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                appointment_id,
                appointment_time,
                status
            FROM appointments
            WHERE doctor_id  = %s
              AND patient_id = %s
              AND status     = 'completed'
            ORDER BY appointment_time DESC
        """, (doctor_id, patient_id))
        apps = cursor.fetchall()
        return jsonify(apps), 200

    except mysql.connector.Error as e:
        print("❌ Error listing appointments:", e)
        return jsonify(error="Internal server error"), 500

    finally:
        cursor.close()
        conn.close()
