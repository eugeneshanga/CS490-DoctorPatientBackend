from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")


# send message
@chat_bp.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    message = data.get('message')

    if not patient_id or not doctor_id or not message:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # pust the chat to database chat_history
        cursor.execute("""
            INSERT INTO chat_history (patient_id, doctor_id, message)
            VALUES (%s, %s, %s)
        """, (patient_id, doctor_id, message))
        connection.commit()

        return jsonify({"message": "Message sent successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# get all the chats
@chat_bp.route('/all', methods=['GET'])
def get_all_chats():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM chat_history ORDER BY sent_at ASC")
        chats = cursor.fetchall()

        return jsonify(chats), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

# get specific doctor and patient chat detail
@chat_bp.route('/conversation/<int:patient_id>/<int:doctor_id>', methods=['GET'])

def get_chat_between_patient_and_doctor(patient_id, doctor_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM chat_history WHERE patient_id = %s AND doctor_id = %s ORDER BY sent_at ASC
        """, (patient_id, doctor_id))
        chats = cursor.fetchall()

        return jsonify(chats), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()
