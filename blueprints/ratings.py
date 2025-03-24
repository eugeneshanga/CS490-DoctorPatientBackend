from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

ratings_bp = Blueprint("ratings", __name__, url_prefix="/api/ratings")


@ratings_bp.route('/rate_doctor', methods=['POST'])
def rate_doctor():
    data = request.get_json()

    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    appointment_id = data.get('appointment_id')
    rating = data.get('rating')
    review = data.get('review', '')

    if not patient_id or not doctor_id or not appointment_id or rating is None:
        return jsonify({"error": "Missing required fields"}), 400
    if rating < 0 or rating > 5:
        return jsonify({"error": "Rating must be between 0 and 5"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print(f"Checking appointment {appointment_id} for patient {patient_id} and doctor {doctor_id}")  # ✅ 调试输出

        # make sure the patient already did apointment
        cursor.execute("""
            SELECT status FROM appointments
            WHERE appointment_id = %s AND patient_id = %s AND doctor_id = %s
        """, (appointment_id, patient_id, doctor_id))
        appointment = cursor.fetchone()

        if not appointment:
            print(f"❌ Appointment {appointment_id} not found for patient {patient_id} and doctor {doctor_id}")  # ✅ 记录错误
            return jsonify({"error": "Appointment not found"}), 404

        if appointment[0].lower() != "completed":  
            print(f"❌ Appointment {appointment_id} is not completed (current status: {appointment[0]})")  # ✅ 调试
            return jsonify({"error": "You can only rate after a completed appointment"}), 403

        print(f"✅ Appointment {appointment_id} is completed. Proceeding with rating.")  # ✅ 继续

        
        cursor.execute("""
            SELECT * FROM ratings WHERE patient_id = %s AND doctor_id = %s AND appointment_id = %s
        """, (patient_id, doctor_id, appointment_id))
        existing_rating = cursor.fetchone()
        if existing_rating:
            return jsonify({"error": "You have already rated this appointment"}), 409

        # 
        cursor.execute("""
            INSERT INTO ratings (patient_id, doctor_id, appointment_id, rating, review)
            VALUES (%s, %s, %s, %s, %s)
        """, (patient_id, doctor_id, appointment_id, rating, review))
        connection.commit()

        # 
        cursor.execute("""
            INSERT INTO doctor_ratings (doctor_id, total_ratings, average_rating)
            VALUES (%s, 1, %s)
            ON DUPLICATE KEY UPDATE
                total_ratings = total_ratings + 1,
                average_rating = ((average_rating * (total_ratings - 1)) + VALUES(average_rating)) / total_ratings;
        """, (doctor_id, rating))
        connection.commit()

        return jsonify({"message": "Rating submitted and doctor rating updated"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()
