from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG
import json

discussion_bp = Blueprint("discussion", __name__, url_prefix="/api/discussion")


# doctoc post
@discussion_bp.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    post_title = data.get('post_title')
    post_content = data.get('post_content')  # ✅ 这里 post_content 需要是字典

    if not doctor_id or not post_title or not post_content:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # json data
        cursor.execute("""
            INSERT INTO discussion_board (doctor_id, post_title, post_content)
            VALUES (%s, %s, %s)
        """, (doctor_id, post_title, json.dumps(post_content)))  # ✅ 需要转换为 JSON 字符串
        connection.commit()

        return jsonify({"message": "Post created successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# get new post
@discussion_bp.route('/posts', methods=['GET'])
def get_all_posts():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM discussion_board ORDER BY created_at DESC")
        posts = cursor.fetchall()

        return jsonify(posts), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# patient reply
@discussion_bp.route('/reply', methods=['POST'])
def reply_to_post():
    data = request.get_json()
    post_id = data.get('post_id')
    patient_id = data.get('patient_id')
    reply_content = data.get('reply_content')

    if not post_id or not patient_id or not reply_content:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # reply
        cursor.execute("""
            INSERT INTO post_replies (post_id, patient_id, reply_content)
            VALUES (%s, %s, %s)
        """, (post_id, patient_id, reply_content))
        connection.commit()

        return jsonify({"message": "Reply submitted successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# get all the post
@discussion_bp.route('/replies/<int:post_id>', methods=['GET'])
def get_post_replies(post_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM post_replies WHERE post_id = %s ORDER BY replied_at ASC
        """, (post_id,))
        replies = cursor.fetchall()

        return jsonify(replies), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()
