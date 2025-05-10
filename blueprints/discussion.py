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

        cursor.execute("""
        SELECT 
            d.*, 
            COUNT(pu.user_id) AS upvote_count
        FROM 
            discussion_board d
        LEFT JOIN 
            post_upvotes pu ON d.post_id = pu.post_id
        GROUP BY 
            d.post_id
        ORDER BY 
            upvote_count DESC, created_at DESC
        """)
        posts = cursor.fetchall()

        return jsonify(posts), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# reply
@discussion_bp.route('/reply', methods=['POST'])
def reply_to_post():
    data = request.get_json()
    post_id = data.get('post_id')
    user_id = data.get('user_id')
    reply_content = data.get('reply_content')

    if not post_id or not user_id or not reply_content:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # reply
        cursor.execute("""
            INSERT INTO post_replies (post_id, user_id, reply_content)
            VALUES (%s, %s, %s)
        """, (post_id, user_id, reply_content))
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


@discussion_bp.route('/reply-comments', methods=['POST'])
def add_reply_to_reply():
    data = request.get_json()
    reply_id = data.get('reply_id')
    user_id = data.get('user_id')
    content = data.get('content')

    if not reply_id or not user_id or not content:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO reply_comments (reply_id, user_id, content)
            VALUES (%s, %s, %s)
        """, (reply_id, user_id, content))
        connection.commit()

        return jsonify({"message": "Reply comment submitted successfully"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


@discussion_bp.route('/reply-comments/<int:reply_id>', methods=['GET'])
def get_reply_comments(reply_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT rc.comment_id AS id, rc.reply_id, rc.user_id, rc.content, rc.commented_at AS created_at, u.email
            FROM reply_comments rc
            JOIN users u ON rc.user_id = u.user_id
            WHERE rc.reply_id = %s
            ORDER BY rc.commented_at ASC
        """, (reply_id,))
        reply_comments = cursor.fetchall()

        return jsonify(reply_comments), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


@discussion_bp.route('/replies/username/<int:user_id>', methods=['GET'])
def get_user_name(user_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT user_type FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_type = user['user_type']
        name = None

        if user_type == 'patient':
            cursor.execute("SELECT first_name, last_name FROM patients WHERE user_id = %s", (user_id,))
            info = cursor.fetchone()
            name = f"{info['first_name']} {info['last_name']}" if info else None

        elif user_type == 'doctor':
            cursor.execute("SELECT first_name, last_name FROM doctors WHERE user_id = %s", (user_id,))
            info = cursor.fetchone()
            name = f"Dr. {info['first_name']} {info['last_name']}" if info else None

        elif user_type == 'pharmacy':
            cursor.execute("SELECT name FROM pharmacies WHERE user_id = %s", (user_id,))
            info = cursor.fetchone()
            name = info['name'] if info else None

        if name:
            return jsonify({"name": name}), 200
        else:
            return jsonify({"error": "User details not found"}), 404

    finally:
        cursor.close()
        connection.close()


@discussion_bp.route('/posts/author/<int:post_id>', methods=['GET'])
def get_post_author_name(post_id):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT d.first_name, d.last_name
            FROM discussion_board db
            JOIN doctors d ON db.doctor_id = d.doctor_id
            WHERE db.post_id = %s
        """, (post_id,))

        result = cursor.fetchone()

        if result:
            return jsonify({"name": f"Dr. {result['first_name']} {result['last_name']}"})
        else:
            return jsonify({"name": "Unknown"})

    finally:
        cursor.close()
        connection.close()


@discussion_bp.route('/api/posts/upvote', methods=['POST'])
def toggle_post_upvote():
    data = request.json
    post_id = data.get('post_id')
    user_id = data.get('user_id')

    if not post_id or not user_id:
        return jsonify({"error": "Missing post_id or user_id"}), 400

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    try:
        # Check if the user has already upvoted the post
        cursor.execute(
            "SELECT * FROM post_upvotes WHERE user_id = %s AND post_id = %s",
            (user_id, post_id)
        )
        existing_upvote = cursor.fetchone()

        if existing_upvote:
            # Remove the upvote
            cursor.execute(
                "DELETE FROM post_upvotes WHERE user_id = %s AND post_id = %s",
                (user_id, post_id)
            )
            connection.commit()
            return jsonify({"status": "removed"})
        else:
            # Add the upvote
            cursor.execute(
                "INSERT INTO post_upvotes (user_id, post_id) VALUES (%s, %s)",
                (user_id, post_id)
            )
            connection.commit()
            return jsonify({"status": "added"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        connection.close()

@discussion_bp.route('/api/posts/upvotes/<int:post_id>', methods=['GET'])
def get_upvote_status(post_id):
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing user_id in query params"}), 400

    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    try:
        # Count total upvotes for the post
        cursor.execute(
            "SELECT COUNT(*) AS count FROM post_upvotes WHERE post_id = %s",
            (post_id,)
        )
        upvote_count = cursor.fetchone()['count']

        # Check if the user has already upvoted
        cursor.execute(
            "SELECT 1 FROM post_upvotes WHERE user_id = %s AND post_id = %s",
            (user_id, post_id)
        )
        user_upvoted = cursor.fetchone() is not None

        return jsonify({
            "count": upvote_count,
            "upvoted": user_upvoted
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        connection.close()
