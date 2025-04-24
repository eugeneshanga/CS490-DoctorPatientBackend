from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

# Create a blueprint for meal plan endpoints
mealplans_bp = Blueprint('mealplans', __name__, url_prefix='/api/patient-dashboard/mealplans')


@mealplans_bp.route('/patient/create', methods=['POST'])
def create_patient_mealplan():
    """
    Create a new patient meal plan.
    Expects a multipart/form-data request with the following fields:
      - user_id: The patient’s user_id (as form field or query param)
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

    # Validate required fields
    if not user_id or not title:
        return jsonify({"error": "Missing required fields: user_id and title are required"}), 400

    # Get the image file from the upload, if provided.
    image_file = request.files.get('image')
    image_data = None
    if image_file:
        # Read the binary data for the image
        image_data = image_file.read()

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Convert user_id to patient_id
        cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found for given user_id"}), 404
        patient_id = patient[0]  # assuming cursor.fetchone() returns a tuple

        insert_sql = """
            INSERT INTO patient_meal_plans
              (patient_id, title, description, image, instructions, calories, fat, sugar, ingredients)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            patient_id,
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
        return jsonify({"message": "Patient meal plan created successfully", "meal_plan_id": meal_plan_id}), 201

    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({"error": str(err)}), 500


@mealplans_bp.route('/patient/all', methods=['GET'])
def get_patient_mealplans():
    """
    Retrieve all meal plans for a given user_id (via query param).
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Look up patient_id using user_id
        cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Patient not found for this user_id"}), 404

        patient_id = result['patient_id']

        # Fetch all mealplans for that patient
        cursor.execute("""
            SELECT meal_plan_id, title, description, instructions, ingredients, calories, fat, sugar
            FROM patient_meal_plans
            WHERE patient_id = %s
        """, (patient_id,))
        mealplans = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"mealplans": mealplans}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@mealplans_bp.route('/delete/<int:meal_plan_id>', methods=['DELETE'])
def delete_mealplan(meal_plan_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM patient_meal_plans WHERE meal_plan_id = %s", (meal_plan_id,))
        connection.commit()

        cursor.close()
        connection.close()
        return jsonify({"message": "Meal plan deleted"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500