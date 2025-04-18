from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")

# send
@chat_bp.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    sender_type = data.get('sender_type')
    message = data.get('message')

    if not patient_id or not doctor_id or not message or not sender_type:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO chat_history (patient_id, doctor_id, sender_type, message)
            VALUES (%s, %s, %s, %s)
        """, (patient_id, doctor_id, sender_type, message))
        conn.commit()

        return jsonify({"message": "Message sent"}), 201

    except Exception as e:
        print("❌ Error inserting message:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


#get 
@chat_bp.route('/history', methods=['GET'])
def get_chat_history():
    doctor_id = request.args.get('doctor_id')
    patient_id = request.args.get('patient_id')

    if not doctor_id or not patient_id:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM chat_history
            WHERE doctor_id = %s AND patient_id = %s
            ORDER BY sent_at ASC
        """, (doctor_id, patient_id))
        messages = cursor.fetchall()
        return jsonify(messages), 200

    except Exception as e:
        print("❌ Error loading messages:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
