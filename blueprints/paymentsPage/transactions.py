from flask import Blueprint, jsonify, request
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


# --- DOCTOR PAYMENT FULFILL w/ details ---
@payment_transaction_bp.route('/payments/doctor/<int:payment_id>/fulfill', methods=['PATCH'])
def fulfill_doctor_payment(payment_id):
    """
    Mark a doctor payment as fulfilled and record the card details used.
    Expects a JSON body with the following fields:
      - cardholder_name: Name on the card (string, required)
      - card_number: Full card number (string, required)
      - exp_month: Two‑digit expiration month (integer 1–12, required)
      - exp_year: Four‑digit expiration year (integer, required)
      - cvv: Three‑ or four‑digit security code (string, required)

    URL path parameter:
      - payment_id: The ID of the doctor payment to fulfill (int)
    """
    data = request.get_json() or {}
    cardholder_name = data.get('cardholder_name')
    card_number     = data.get('card_number')
    exp_month       = data.get('exp_month')
    exp_year        = data.get('exp_year')
    cvv             = data.get('cvv')

    if not all([cardholder_name, card_number, exp_month, exp_year, cvv]):
        return jsonify({"error": "Missing payment detail fields"}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1) Mark the payment fulfilled
        cursor.execute("""
            UPDATE payments_doctor
               SET is_fulfilled = TRUE
             WHERE payment_id = %s
               AND is_fulfilled = FALSE
        """, (payment_id,))
        if cursor.rowcount == 0:
            conn.rollback()
            return jsonify({"error": "No unfulfilled payment found"}), 404

        # 2) Record the card details
        cursor.execute("""
            INSERT INTO doctor_payment_details
              (payment_id, cardholder_name, card_number, exp_month, exp_year, cvv)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            payment_id,
            cardholder_name,
            card_number,
            exp_month,
            exp_year,
            cvv
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Payment fulfilled and details recorded",
            "payment_id": payment_id
        }), 200

    except mysql.connector.Error as err:
        conn.rollback()
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


# --- PHARMACY PAYMENT FULFILL w/ details ---
@payment_transaction_bp.route(
    '/payments/pharmacy/<int:payment_id>/fulfill', methods=['PATCH']
)
def fulfill_pharmacy_payment(payment_id):
    """
    Mark a pharmacy payment as fulfilled and record the card details used.
    Expects a JSON body with the following fields:
      - cardholder_name: Name on the card (string, required)
      - card_number: Full card number (string, required)
      - exp_month: Two‑digit expiration month (integer 1–12, required)
      - exp_year: Four‑digit expiration year (integer, required)
      - cvv: Three‑ or four‑digit security code (string, required)

    URL path parameter:
      - payment_id: The ID of the pharmacy payment to fulfill (int)
    """
    data = request.get_json() or {}
    cardholder_name = data.get('cardholder_name')
    card_number     = data.get('card_number')
    exp_month       = data.get('exp_month')
    exp_year        = data.get('exp_year')
    cvv             = data.get('cvv')

    if not all([cardholder_name, card_number, exp_month, exp_year, cvv]):
        return jsonify({"error": "Missing payment detail fields"}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1) Mark the payment fulfilled
        cursor.execute("""
            UPDATE payments_pharmacy
               SET is_fulfilled = TRUE
             WHERE payment_id = %s
               AND is_fulfilled = FALSE
        """, (payment_id,))
        if cursor.rowcount == 0:
            conn.rollback()
            return jsonify({"error": "No unfulfilled payment found"}), 404

        # 2) Record the card details
        cursor.execute("""
            INSERT INTO pharmacy_payment_details
              (payment_id, cardholder_name, card_number, exp_month, exp_year, cvv)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            payment_id,
            cardholder_name,
            card_number,
            exp_month,
            exp_year,
            cvv
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Payment fulfilled and details recorded",
            "payment_id": payment_id
        }), 200

    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"error": str(err)}), 500
