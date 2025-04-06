from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

doctor_dashboard_bp = Blueprint('doctor_dashboard', __name__, url_prefix='/api/doctor-dashboard')

@doctor_dashboard_bp.route('/details', methods=['GET'])
def get_doctor_details():
    """
    Endpoint to retrieve doctor details for a given user_id.
    Expects a query parameter 'user_id'. Converts user_id to doctor_id,
    then retrieves first_name, last_name, and doctor_id from the doctors table.
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT doctor_id, first_name, last_name FROM doctors WHERE user_id = %s",
            (user_id,)
        )
        doctor = cursor.fetchone()
        if not doctor:
            return jsonify({"error": "Doctor not found for given user_id"}), 404

        cursor.close()
        connection.close()

        return jsonify({"doctor": doctor}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
