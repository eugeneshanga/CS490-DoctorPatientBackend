from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG
from werkzeug.utils import secure_filename

doctor_dashboard_meal_plans_bp = Blueprint('doctor_dashboard_meal_plans', __name__, url_prefix='/api/doctor-dashboard')

@doctor_dashboard_meal_plans_bp.route('/official/create', methods=['POST'])
def create_official_mealplan():
    user_id = request.form.get('user_id', type=int)
    title = request.form.get('title')
    description = request.form.get('description')
    instructions = request.form.get('instructions')
    calories = request.form.get('calories', type=int)
    fat = request.form.get('fat', type=int)
    sugar = request.form.get('sugar', type=int)
    ingredients = request.form.get('ingredients')

    if not user_id or not title:
        return jsonify({"error": "Missing required fields: user_id and title are required"}), 400

    image_file = request.files.get('image')
    image_data = None
    if image_file:
        filename = secure_filename(image_file.filename)  # noqa: F841
        image_data = image_file.read()

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # ✅ Hardcoded for testing
        doctor_id = 1

        insert_sql = """
            INSERT INTO official_meal_plans
              (doctor_id, title, description, image, instructions, calories, fat, sugar, ingredients)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            doctor_id,
            title,
            description,
            image_data,
            instructions,
            calories,
            fat,
            sugar,
            ingredients
        )
        cursor.execute(insert_sql, values)
        connection.commit()
        meal_plan_id = cursor.lastrowid

        cursor.close()
        connection.close()
        return jsonify({"message": "Official meal plan created successfully", "meal_plan_id": meal_plan_id}), 201

    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({"error": str(err)}), 500


@doctor_dashboard_meal_plans_bp.route('/official/all', methods=['GET'])
def get_official_mealplans():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # ✅ Hardcoded doctor_id for testing
        doctor_id = 1

        cursor.execute("""
            SELECT meal_plan_id, title, description, instructions, ingredients,
                   calories, fat, sugar
            FROM official_meal_plans
            WHERE doctor_id = %s
        """, (doctor_id,))
        mealplans = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"mealplans": mealplans}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500