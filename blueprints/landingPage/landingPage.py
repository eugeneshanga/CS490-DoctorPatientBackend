from flask import Blueprint, jsonify
import mysql.connector
from config import DB_CONFIG

pharmacy_bp = Blueprint('pharmacy', __name__, url_prefix='/api/pharmacies')
doctor_bp = Blueprint('doctor', __name__, url_prefix='/api/doctors')

# Blueprint for Doctors


@doctor_bp.route('/all', methods=['GET'])
def get_all_doctors():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # ✅ Get doctor info + average rating
        cursor.execute("""
            SELECT
                d.doctor_id,
                d.first_name,
                d.last_name,
                d.address,
                d.phone_number,
                d.description,
                IFNULL(AVG(r.rating), 0) AS average_rating
            FROM doctors d
            LEFT JOIN ratings r ON d.doctor_id = r.doctor_id
            GROUP BY d.doctor_id
        """)

        rows = cursor.fetchall()

        doctors = [
            {
                "doctor_id": row["doctor_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "address": row["address"],
                "phone_number": row["phone_number"],
                "description": row["description"],
                "average_rating": float(row["average_rating"])  # Safely send as JSON number
            }
            for row in rows
        ]

        cursor.close()
        connection.close()

        return jsonify({"doctors": doctors}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


# Blueprint for Pharmacies
@pharmacy_bp.route('/all', methods=['GET'])
def get_all_pharmacies():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # ✅ Use correct column name from schema: 'name', not 'pharmacy_name'
        cursor.execute("SELECT pharmacy_id, name, address, phone_number FROM pharmacies")
        rows = cursor.fetchall()

        # ✅ Format response as if it still had 'pharmacy_name' for frontend consistency
        pharmacies = [
            {
                "pharmacy_id": row["pharmacy_id"],
                "pharmacy_name": row["name"],
                "address": row["address"],
                "phone_number": row["phone_number"]
            }
            for row in rows
        ]

        cursor.close()
        connection.close()

        return jsonify({"pharmacies": pharmacies}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
