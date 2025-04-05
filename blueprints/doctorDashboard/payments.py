from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

doctor_dashboard_payments_bp = Blueprint('doctor_dashboard_payments', __name__, url_prefix='/api/doctor-dashboard')


@doctor_dashboard_payments_bp.route('/payments', methods=['GET'])
def get_doctor_payments():
    """
    Endpoint for a doctor to fetch all payments received from patients.
    Expects a query parameter 'user_id' representing the doctor's user ID.
    Converts the user_id to doctor_id and retrieves payments from the payments_doctor table.
    Each payment record includes:
      - payment_id
      - patient's first_name and last_name (from patients table)
      - amount
      - is_fulfilled
      - payment_date
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

        # Retrieve all payments for the doctor by joining with patients for additional details
        sql = """
            SELECT pd.payment_id, p.first_name, p.last_name, pd.amount, pd.is_fulfilled, pd.payment_date
            FROM payments_doctor pd
            JOIN patients p ON pd.patient_id = p.patient_id
            WHERE pd.doctor_id = %s
            ORDER BY pd.payment_date DESC
        """
        cursor.execute(sql, (doctor_id,))
        payments = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"payments": payments}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
