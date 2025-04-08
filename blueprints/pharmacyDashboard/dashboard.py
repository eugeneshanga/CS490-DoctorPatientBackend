from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

pharmacy_dashboard_bp = Blueprint('pharmacy_dashboard', __name__, url_prefix='/api/pharmacy-dashboard')


@pharmacy_dashboard_bp.route('/details', methods=['GET'])
def get_pharmacy_details():
    """
    Endpoint to retrieve pharmacy details for a given user_id.
    Expects a query parameter 'user_id'.
    Converts user_id to the corresponding pharmacy record in the pharmacies table.
    Returns: pharmacy_id, name, phone_number, and license_number.
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT pharmacy_id, name, phone_number, license_number FROM pharmacies WHERE user_id = %s",
            (user_id,)
        )
        pharmacy = cursor.fetchone()
        if not pharmacy:
            return jsonify({"error": "Pharmacy not found for given user_id"}), 404

        cursor.close()
        connection.close()

        return jsonify({"pharmacy": pharmacy}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
