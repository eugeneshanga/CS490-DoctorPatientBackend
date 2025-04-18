from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG
from werkzeug.utils import secure_filename

doctor_dashboard_meal_plans_bp = Blueprint('doctor_dashboard_meal_plans', __name__, url_prefix='/api/doctor-dashboard')


@doctor_dashboard_meal_plans_bp.route('/official/create', methods=['POST'])
def create_official_mealplan():
    """
    Create a new official meal plan.
    Expects a multipart/form-data request with the following fields:
      - user_id: The doctor's user_id (as form field or query param)
      - title: The title of the meal plan (string, required)
      - description: Description of the meal (optional)
      - instructions: Preparation/serving instructions (optional)
      - calories: Numeric value for calories (optional)
      - fat: Numeric value for fat content (optional)
      - sugar: Numeric value for sugar content (optional)
      - ingredients: A comma-separated list of ingredients (string, optional)
      - image: The image file to upload (optional)
    """
    # Get form fields
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

        # Convert user_id to doctor_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        if not doctor:
            return jsonify({"error": "Doctor not found for given user_id"}), 404
        doctor_id = doctor[0]

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
