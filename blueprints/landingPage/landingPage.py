from flask import Blueprint, jsonify
import mysql.connector
from config import DB_CONFIG

pharmacy_bp = Blueprint('pharmacy', __name__, url_prefix='/api/pharmacies')


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
