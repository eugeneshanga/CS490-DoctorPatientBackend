from flask import Blueprint, request, jsonify
import mysql.connector
import bcrypt
from config import DB_CONFIG
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route('/login', methods=['POST'])



def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')  
    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)  
        cursor.execute("""
            SELECT user_id, email, password_hash, user_type FROM users WHERE email = %s
        """, (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({"error": "Invalid email or password"}), 401
        return jsonify({
            "message": "Login successful",
            "user": {
                "user_id": user["user_id"],
                "email": user["email"],
                "user_type": user["user_type"]
            }
        }), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()
