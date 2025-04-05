from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

doctor_dashboard_meal_plans_bp = Blueprint('doctor_dashboard_meal_plans', __name__, url_prefix='/api/doctor-dashboard')

@doctor_dashboard_meal_plans_bp.route('/official-meal-plans', methods=['GET'])
def get_official_meal_plans():
    """
    Endpoint for a doctor to fetch all official meal plans they have created.
    Expects a query parameter 'user_id' representing the doctor's user ID.
    Converts the user_id to doctor_id, then retrieves all official meal plans.

    Returns:
      A JSON object with a key "official_meal_plans" that is an array of meal plans.
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

        # Retrieve all official meal plans created by this doctor
        sql = """
            SELECT meal_plan_id, doctor_id, title, description, meal_plan, created_at
            FROM official_meal_plans
            WHERE doctor_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (doctor_id,))
        meal_plans = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"official_meal_plans": meal_plans}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

