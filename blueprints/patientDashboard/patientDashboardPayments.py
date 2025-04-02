from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

patient_dashboard_payments_bp = Blueprint('patient_dashboard_payments', __name__, url_prefix='/api/patient-dashboard/payments')


@patient_dashboard_payments_bp.route('/doctor', methods=['GET'])
def get_doctor_payments():
    """
    Endpoint to fetch all payments made by a patient to doctors.
    Now expects a query parameter `user_id`, converts it to patient_id,
    and returns: payment_id, doctor's first & last name, amount, payment status, and payment date.
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

        # Join payments_doctor with doctors to get doctor's name for display
        sql = """
            SELECT pd.payment_id, d.first_name, d.last_name, pd.amount, pd.is_fulfilled, pd.payment_date
            FROM payments_doctor pd
            JOIN doctors d ON pd.doctor_id = d.doctor_id
            WHERE pd.patient_id = %s
            ORDER BY pd.payment_date DESC
        """
        cursor.execute(sql, (patient_id,))
        payments = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(payments), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
