from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG
from werkzeug.utils import secure_filename

doctor_mealplans_bp = Blueprint('doctor_mealplans', __name__)


@doctor_mealplans_bp.route('/api/doctor-dashboard/official/create', methods=['POST'])
def create_doctor_mealplan():
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


@doctor_mealplans_bp.route('/api/doctor-dashboard/official/all', methods=['GET'])
def get_doctor_mealplans():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Doctor not found"}), 404
        doctor_id = result[0]

        cursor.execute("""
            SELECT meal_plan_id, title, description, ingredients, instructions,
                   calories, fat, sugar, image
            FROM official_meal_plans
            WHERE doctor_id = %s
        """, (doctor_id,))
        rows = cursor.fetchall()

        mealplans = []
        for row in rows:
            mealplans.append({
                "meal_plan_id": row[0],
                "title": row[1],
                "description": row[2],
                "ingredients": row[3],
                "instructions": row[4],
                "calories": row[5],
                "fat": row[6],
                "sugar": row[7],
                "image": row[8].decode('utf-8') if row[8] else None
            })

        return jsonify(mealplans), 200
    except Exception as e:
        print("Error fetching doctor mealplans:", e)
        return jsonify({"error": "Internal server error"}), 500


@doctor_mealplans_bp.route('/api/doctor-dashboard/official/delete', methods=['POST'])
def delete_doctor_mealplan():
    meal_plan_id = request.form.get("meal_plan_id")

    if not meal_plan_id:
        return jsonify({"error": "Missing meal_plan_id"}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM official_meal_plans WHERE meal_plan_id = %s", (meal_plan_id,))
        mysql.connection.commit()

        return jsonify({"message": "Mealplan deleted successfully"}), 200
    except Exception as e:
        print("Error deleting mealplan:", e)
        return jsonify({"error": "Internal server error"}), 500
