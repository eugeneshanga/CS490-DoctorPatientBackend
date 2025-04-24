from flask import Blueprint, request, jsonify
import mysql.connector
import base64
from config import DB_CONFIG

doctor_mealplans_bp = Blueprint('doctor_mealplans_bp', __name__)

# CREATE MEAL PLAN
@doctor_mealplans_bp.route("/doctor-dashboard/official/create", methods=["POST"])
def create_official_meal_plan():
    try:
        user_id = request.form.get("user_id")
        title = request.form.get("title")
        description = request.form.get("description")
        instructions = request.form.get("instructions")
        ingredients = request.form.get("ingredients")
        calories = request.form.get("calories")
        fat = request.form.get("fat")
        sugar = request.form.get("sugar")
        image_file = request.files.get("image")
        image_data = image_file.read() if image_file else None

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        doctor_id = doctor[0] if doctor else None

        print("📥 Creating meal plan for doctor_id:", doctor_id)

        if not doctor_id:
            return jsonify({"error": "Doctor not found for this user_id"}), 404

        cursor.execute("""
            INSERT INTO official_meal_plans
            (doctor_id, title, description, instructions, ingredients, calories, fat, sugar, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (doctor_id, title, description, instructions, ingredients, calories, fat, sugar, image_data))
        connection.commit()

        return jsonify({"message": "Meal plan created successfully"}), 201

    except Exception as e:
        print("🔥 Error in create_official_meal_plan:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

# GET ALL MEAL PLANS FOR A DOCTOR
@doctor_mealplans_bp.route("/doctor-dashboard/official/all", methods=["GET"])
def get_official_meal_plans():
    try:
        user_id = request.args.get("user_id")
        print("📡 Fetching meal plans for user_id:", user_id)

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        doctor_id = doctor[0] if doctor else None

        print("👨‍⚕️ Resolved doctor_id:", doctor_id)

        if not doctor_id:
            return jsonify({"mealplans": []}), 200

        cursor.execute("""
            SELECT meal_plan_id, title, description, instructions, ingredients, calories, fat, sugar, image
            FROM official_meal_plans
            WHERE doctor_id = %s
        """, (doctor_id,))
        result = cursor.fetchall()

        print("✅ Mealplans fetched:", result)

        mealplans = []
        for row in result:
            mealplans.append({
                "meal_plan_id": row[0],
                "title": row[1],
                "description": row[2],
                "instructions": row[3],
                "ingredients": row[4],
                "calories": row[5],
                "fat": row[6],
                "sugar": row[7],
                "image": base64.b64encode(row[8]).decode('utf-8') if row[8] else None
            })

        return jsonify({"mealplans": mealplans}), 200

    except Exception as e:
        print("🔥 Error in get_official_meal_plans:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

# DELETE MEAL PLAN
@doctor_mealplans_bp.route("/doctor-dashboard/official/delete/<int:meal_plan_id>", methods=["DELETE"])
def delete_official_meal_plan(meal_plan_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM official_meal_plans WHERE meal_plan_id = %s", (meal_plan_id,))
        connection.commit()

        return jsonify({"message": "Meal plan deleted successfully"}), 200

    except Exception as e:
        print("🔥 Error in delete_official_meal_plan:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass