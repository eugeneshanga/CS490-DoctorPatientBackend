from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

pharmacy_dashboard_payments_bp = Blueprint('pharmacy_dashboard_payments', __name__, url_prefix='/api/pharmacy-dashboard/payments')


@pharmacy_dashboard_payments_bp.route('/list', methods=['GET'])
def get_pharmacy_payments():
    """
    Endpoint to fetch all payment transactions for a pharmacy.
    Expects a query parameter 'user_id', converts it to pharmacy_id,
    then retrieves all payments from the payments_pharmacy table joined with the patients table.
    Returns a JSON object with a key "payments" that is an array of payment records containing:
      - payment_id
      - patient's first_name and last_name
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

        # Convert user_id to pharmacy_id
        cursor.execute("SELECT pharmacy_id FROM pharmacies WHERE user_id = %s", (user_id,))
        pharmacy = cursor.fetchone()
        if not pharmacy:
            return jsonify({"error": "Pharmacy not found for given user_id"}), 404
        pharmacy_id = pharmacy["pharmacy_id"]

        # Retrieve all payments for this pharmacy, joined with patient details
        sql = """
            SELECT pp.payment_id, p.first_name, p.last_name, pp.amount, pp.is_fulfilled, pp.payment_date
            FROM payments_pharmacy pp
            JOIN patients p ON pp.patient_id = p.patient_id
            WHERE pp.pharmacy_id = %s
            ORDER BY pp.payment_date DESC
        """
        cursor.execute(sql, (pharmacy_id,))
        payments = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"payments": payments}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
