from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

patient_dashboard_payments_bp = Blueprint('patient_dashboard_payments', __name__, url_prefix='/api/patient-dashboard/payments')


@patient_dashboard_payments_bp.route('/doctor', methods=['GET'])
def get_doctor_payments():
    """
    Endpoint to fetch all payments made by a patient to doctors.
    Returns: payment_id, doctor's first & last name, amount, payment status, and payment date.
    """
    patient_id = request.args.get('patient_id', type=int)
    if not patient_id:
        return jsonify({"error": "patient_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

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


@patient_dashboard_payments_bp.route('/pharmacy', methods=['GET'])
def get_pharmacy_payments():
    """
    Endpoint to fetch all payments made by a patient to pharmacies.
    Returns: payment_id, pharmacy name, amount, payment status, and payment date.
    """
    patient_id = request.args.get('patient_id', type=int)
    if not patient_id:
        return jsonify({"error": "patient_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Join payments_pharmacy with pharmacies to get the pharmacy name
        sql = """
            SELECT pp.payment_id, p.name AS pharmacy_name, pp.amount, pp.is_fulfilled, pp.payment_date
            FROM payments_pharmacy pp
            JOIN pharmacies p ON pp.pharmacy_id = p.pharmacy_id
            WHERE pp.patient_id = %s
            ORDER BY pp.payment_date DESC
        """
        cursor.execute(sql, (patient_id,))
        payments = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(payments), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
