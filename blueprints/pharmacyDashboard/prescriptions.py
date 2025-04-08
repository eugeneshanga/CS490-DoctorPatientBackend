from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

pharmacy_dashboard_prescriptions_bp = Blueprint('pharmacy_dashboard_prescriptions', __name__,
                                                url_prefix='/api/pharmacy-dashboard/prescriptions')


@pharmacy_dashboard_prescriptions_bp.route('/list-all', methods=['GET'])
def get_prescriptions():
    """
    Endpoint to fetch all prescriptions associated with the pharmacy.
    Expects a query parameter 'user_id', converts it to pharmacy_id,
    and retrieves all prescriptions for that pharmacy.
    Returns a JSON array of prescription records with fields such as:
      - prescription_id
      - doctor_id
      - patient_id
      - pharmacy_id
      - medication_name
      - dosage
      - instructions
      - status
      - created_at
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

        # Query the prescriptions table for this pharmacy's prescriptions
        sql = """
            SELECT prescription_id, doctor_id, patient_id, pharmacy_id, medication_name,
                   dosage, instructions, status, created_at
            FROM prescriptions
            WHERE pharmacy_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (pharmacy_id,))
        prescriptions = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(prescriptions), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
