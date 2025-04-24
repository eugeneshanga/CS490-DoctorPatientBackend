from flask import Blueprint, jsonify, request, send_file
import mysql.connector
from config import DB_CONFIG
from io import BytesIO

# Blueprint for doctor meal plan endpoints
doctor_mealplans_bp = Blueprint('doctor_mealplans', __name__, url_prefix='/api/doctor-dashboard/official')


@doctor_mealplans_bp.route('/create', methods=['POST'])
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
    #Get form fields
    user_id = request.form.get('user_id', type=int)
    title = request.form.get('title')
    description = request.form.get('description')
    instructions = request.form.get('instructions')
    calories = request.form.get('calories', type=int)
    fat = request.form.get('fat', type=int)
    sugar = request.form.get('sugar', type=int)
    ingredients = request.form.get('ingredients')

    # Get the image file from the upload, if provided.
    image_file = request.files.get('image')
    image_data = image_file.read() if image_file else None

    # Validate required fields
    if not user_id or not title:
        return jsonify({"error": "Missing required fields: user_id and title are required"}), 400

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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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


@doctor_mealplans_bp.route('/all', methods=['GET'])
def get_doctor_mealplans():
    """
    Retrieve all official meal plans for a given doctor user_id (via query param).
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Convert user_id to doctor_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Doctor not found"}), 404

        doctor_id = result[0]

        # Fetch all meal plans
        cursor.execute("""
        new-pharmacy
            SELECT meal_plan_id, title, description, ingredients, instructions, 
                   calories, fat, sugar
                   
            SELECT meal_plan_id, title, description, ingredients, instructions,
                   calories, fat, sugar, image
        main
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
                "sugar": row[7]
            })

        cursor.close()
        connection.close()

        return jsonify(mealplans), 200
    except Exception as e:
        print("Error fetching doctor mealplans:", e)
        return jsonify({"error": "Internal server error"}), 500

        new-pharmacy


@doctor_mealplans_bp.route('/api/doctor-dashboard/official/delete', methods=['POST'])
def delete_doctor_mealplan():
    meal_plan_id = request.form.get("meal_plan_id")

    if not meal_plan_id:
        return jsonify({"error": "Missing meal_plan_id"}), 400
        main

@doctor_mealplans_bp.route('/delete/<int:meal_plan_id>', methods=['DELETE'])
def delete_doctor_mealplan(meal_plan_id):
    """
    Delete an official meal plan by ID.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM official_meal_plans WHERE meal_plan_id = %s", (meal_plan_id,))
        connection.commit()

        cursor.close()
        connection.close()
        return jsonify({"message": "Mealplan deleted successfully"}), 200
    except Exception as e:
        print("Error deleting mealplan:", e)
        return jsonify({"error": "Internal server error"}), 500
        new-pharmacy


@doctor_mealplans_bp.route('/image/<int:meal_plan_id>', methods=['GET'])
def get_mealplan_image(meal_plan_id):
    """
    Serve the image for a given meal plan ID.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT image FROM official_meal_plans WHERE meal_plan_id = %s", (meal_plan_id,))
        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if not row or not row[0]:
            return jsonify({"error": "Image not found"}), 404

        return send_file(BytesIO(row[0]), mimetype='image/jpeg')

    except Exception as e:
        print("Error serving image:", e)
        return jsonify({"error": "Internal server error"}), 500

        main
