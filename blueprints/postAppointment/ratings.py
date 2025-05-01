from flask import Blueprint, request, jsonify, current_app
import mysql.connector
from config import DB_CONFIG

ratings_bp = Blueprint("ratings", __name__, url_prefix="/api/post-appointment/ratings")


@ratings_bp.route('/rate_doctor', methods=['POST'])
def rate_doctor():
    # 1) Ensure JSON body
    if not request.is_json:
        return jsonify(error="Request body must be JSON"), 400

    data = request.get_json()

    # 2) Required fields
    required = ['patient_id', 'doctor_id', 'appointment_id', 'rating']
    missing = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify(error=f"Missing required field(s): {', '.join(missing)}"), 400

    # 3) Parse and validate types
    try:
        patient_id = int(data['patient_id'])
        doctor_id = int(data['doctor_id'])
        appointment_id = int(data['appointment_id'])
    except (ValueError, TypeError):
        return jsonify(error="patient_id, doctor_id and appointment_id must be integers"), 400

    try:
        rating = float(data['rating'])
    except (ValueError, TypeError):
        return jsonify(error="rating must be a number between 0 and 5"), 400

    review = data.get('review', '')
    if not isinstance(review, str):
        return jsonify(error="review must be a string"), 400
    if len(review) > 1000:
        return jsonify(error="review cannot exceed 1000 characters"), 400

    # 4) Enforce rating range
    if rating < 0 or rating > 5:
        return jsonify(error="rating must be between 0 and 5"), 400

    # 5) Database operations
    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                # 5a) Verify appointment exists and is completed
                cur.execute("""
                    SELECT status
                      FROM appointments
                     WHERE appointment_id=%s
                       AND patient_id=%s
                       AND doctor_id=%s
                """, (appointment_id, patient_id, doctor_id))
                row = cur.fetchone()
                if not row:
                    return (
                        jsonify(
                            error=(
                                f"Appointment {appointment_id} not found "
                                f"for patient {patient_id} and doctor {doctor_id}"
                            )
                        ),
                        404
                    )
                status = row[0].lower()
                if status != 'completed':
                    return (
                        jsonify(
                            error=(
                                f"Cannot rate appointment {appointment_id} "
                                f"in status '{row[0]}'; only completed appointments can be rated"
                            )
                        ),
                        403
                    )

                # 5b) Prevent duplicate rating
                cur.execute("""
                    SELECT 1
                      FROM ratings
                     WHERE patient_id=%s
                       AND doctor_id=%s
                       AND appointment_id=%s
                """, (patient_id, doctor_id, appointment_id))
                if cur.fetchone():
                    return (
                        jsonify(
                            error=(
                                f"Rating already exists for "
                                f"appointment {appointment_id}"
                            )
                        ),
                        409
                    )

                # 5c) Insert new rating
                cur.execute("""
                    INSERT INTO ratings
                      (patient_id, doctor_id, appointment_id, rating, review)
                    VALUES (%s, %s, %s, %s, %s)
                """, (patient_id, doctor_id, appointment_id, rating, review))

                # 5d) Update aggregate doctor_ratings
                cur.execute("""
                    INSERT INTO doctor_ratings
                      (doctor_id, total_ratings, average_rating)
                    VALUES (%s, 1, %s)
                    ON DUPLICATE KEY UPDATE
                      average_rating = (
                        average_rating * total_ratings + VALUES(average_rating)
                      ) / (total_ratings + 1),
                      total_ratings = total_ratings + 1
                """, (doctor_id, rating))

            conn.commit()

        return jsonify(message="Rating submitted successfully"), 201

    except mysql.connector.Error as err:
        # Log full details server‑side; hide them from clients
        current_app.logger.error("DB error in rate_doctor: %s", err)
        return jsonify(error="Internal server error"), 500
