from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

results_bp = Blueprint('doctor_payments', __name__, url_prefix='/api/doctor-dashboard/payments')


@results_bp.route('/create', methods=['POST'])
def create_payment():
    """
    Create a new payment record for a just‑completed appointment.
    Expects JSON body with:
      - doctor_id:       INT
      - patient_id:      INT
      - appointment_id:  INT
      - amount:          FLOAT
    """
    data = request.get_json() or {}
    doctor_id = data.get('doctor_id')
    patient_id = data.get('patient_id')
    appointment_id = data.get('appointment_id')
    amount = data.get('amount')

    if not all([doctor_id, patient_id, appointment_id, amount]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert into payments_doctor
        cursor.execute("""
            INSERT INTO payments_doctor (doctor_id, patient_id, amount)
            VALUES (%s, %s, %s)
        """, (doctor_id, patient_id, amount))
        conn.commit()

        payment_id = cursor.lastrowid
        return jsonify({
            "payment_id": payment_id,
            "message": "Payment created successfully."
        }), 201

    except Exception as e:
        print("❌ Error creating payment:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
