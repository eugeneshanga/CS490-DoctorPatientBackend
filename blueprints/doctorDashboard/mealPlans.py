from flask import Blueprint, request, jsonify
import mysql.connector
import base64
from config import DB_CONFIG
import os

# Lets images be rendered to demoData
UPLOAD_FOLDER = 'static/images'

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
        
        if image_file:
            # Save the uploaded file into static/images
            image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
            image_file.save(image_path)
            image_data = f"images/{image_file.filename}"
        else:
            image_data = None

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
                "image": row[8] if row[8] else None
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

# ASSIGN MEAL PLAN TO PATIENTS
@doctor_mealplans_bp.route("/doctor-dashboard/assign-mealplan", methods=["POST"])
def assign_mealplan_to_patient():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        patient_id = data.get("patient_id")
        meal_plan_id = data.get("meal_plan_id")

        if not (user_id and patient_id and meal_plan_id):
            return jsonify({"error": "Missing fields"}), 400

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Get the doctor_id from the user_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE user_id = %s", (user_id,))
        doctor = cursor.fetchone()
        doctor_id = doctor[0] if doctor else None

        if not doctor_id:
            return jsonify({"error": "Doctor not found for this user_id"}), 404

        # Insert assignment into the database
        cursor.execute("""
            INSERT INTO doctor_assign_patient_mealplan (doctor_id, patient_id, meal_plan_id)
            VALUES (%s, %s, %s)
        """, (doctor_id, patient_id, meal_plan_id))
        connection.commit()

        return jsonify({"message": "Meal plan assigned successfully"}), 201

    except Exception as e:
        print("🔥 Error assigning meal plan:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
        

@doctor_mealplans_bp.route("/api/patient-dashboard/assigned-mealplans", methods=["GET"])
def get_assigned_mealplans():
    try:
        user_id = request.args.get("user_id")
        print("📡 Fetching assigned mealplans for user_id:", user_id)

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Find patient_id
        cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"mealplans": []}), 200
        
        patient_id = patient[0]

        # NOW join assignment + doctor + mealplan
        cursor.execute("""
            SELECT dap.assignment_id,
                   d.first_name,
                   d.last_name,
                   dap.assigned_at,
                   omp.title,
                   omp.description,
                   omp.instructions,
                   omp.ingredients,
                   omp.calories,
                   omp.fat,
                   omp.sugar,
                   omp.image
            FROM doctor_assign_patient_mealplan dap
            JOIN official_meal_plans omp ON dap.meal_plan_id = omp.meal_plan_id
            JOIN doctors d ON dap.doctor_id = d.doctor_id
            WHERE dap.patient_id = %s
        """, (patient_id,))

        result = cursor.fetchall()

        mealplans = []
        for row in result:
            mealplans.append({
                "assignment_id": row[0],
                "doctor_name": f"Dr. {row[1]} {row[2]}",
                "assigned_at": row[3].strftime("%Y-%m-%d %H:%M:%S") if row[3] else None,
                "title": row[4],
                "description": row[5],
                "instructions": row[6],
                "ingredients": row[7],
                "calories": row[8],
                "fat": row[9],
                "sugar": row[10],
                "image": row[11] if row[11] else None
            })

        return jsonify({"mealplans": mealplans}), 200

    except Exception as e:
        print("🔥 Error fetching assigned mealplans:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass