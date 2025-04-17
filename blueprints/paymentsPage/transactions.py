from flask import Blueprint, jsonify
import mysql.connector
from config import DB_CONFIG

payment_transaction_bp = Blueprint('payment_transaction', __name__, url_prefix='/api/payment/transaction')


# --- DOCTOR PAYMENT DETAILS ---
@payment_transaction_bp.route('/payments/doctor/<int:payment_id>', methods=['GET'])
def get_doctor_payment(payment_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT
                p.payment_id,
                p.doctor_id,
                d.first_name AS doctor_first_name,
                d.last_name  AS doctor_last_name,
                p.patient_id,
                p.amount,
                p.is_fulfilled,
                p.payment_date
            FROM payments_doctor p
            JOIN doctors d ON p.doctor_id = d.doctor_id
            WHERE p.payment_id = %s
        """
        cursor.execute(sql, (payment_id,))
        payment = cursor.fetchone()
        cursor.close()
        conn.close()

        if not payment:
            return jsonify({"error": "Payment not found"}), 404

        # convert tinyint to bool if needed
        payment['is_fulfilled'] = bool(payment['is_fulfilled'])
        return jsonify(payment), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# --- DOCTOR PAYMENT FULFILL ---
@payment_transaction_bp.route('/payments/doctor/<int:payment_id>/fulfill', methods=['PATCH'])
def fulfill_doctor_payment(payment_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # flip to TRUE only if it exists and is not already fulfilled
        sql = """
            UPDATE payments_doctor
               SET is_fulfilled = TRUE
             WHERE payment_id = %s
               AND is_fulfilled = FALSE
        """
        cursor.execute(sql, (payment_id,))
        conn.commit()
        updated = cursor.rowcount
        cursor.close()
        conn.close()

        if updated == 0:
            return jsonify({"error": "No unfulfilled payment found with that ID"}), 404

        return jsonify({
            "message": "Payment marked as fulfilled",
            "payment_id": payment_id
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# --- PHARMACY PAYMENT DETAILS ---
@payment_transaction_bp.route('/payments/pharmacy/<int:payment_id>', methods=['GET'])
def get_pharmacy_payment(payment_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT
                p.payment_id,
                p.pharmacy_id,
                ph.name       AS pharmacy_name,
                p.patient_id,
                p.amount,
                p.is_fulfilled,
                p.payment_date
            FROM payments_pharmacy p
            JOIN pharmacies ph ON p.pharmacy_id = ph.pharmacy_id
            WHERE p.payment_id = %s
        """
        cursor.execute(sql, (payment_id,))
        payment = cursor.fetchone()
        cursor.close()
        conn.close()

        if not payment:
            return jsonify({"error": "Payment not found"}), 404

        payment['is_fulfilled'] = bool(payment['is_fulfilled'])
        return jsonify(payment), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# --- PHARMACY PAYMENT FULFILL ---
@payment_transaction_bp.route('/payments/pharmacy/<int:payment_id>/fulfill', methods=['PATCH'])
def fulfill_pharmacy_payment(payment_id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = """
            UPDATE payments_pharmacy
               SET is_fulfilled = TRUE
             WHERE payment_id = %s
               AND is_fulfilled = FALSE
        """
        cursor.execute(sql, (payment_id,))
        conn.commit()
        updated = cursor.rowcount
        cursor.close()
        conn.close()

        if updated == 0:
            return jsonify({"error": "No unfulfilled payment found with that ID"}), 404

        return jsonify({
            "message": "Payment marked as fulfilled",
            "payment_id": payment_id
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
