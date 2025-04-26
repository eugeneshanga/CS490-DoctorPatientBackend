# getDoctorReviews.py
from flask import Blueprint, jsonify
import mysql.connector
from config import DB_CONFIG

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@reviews_bp.route('/top-doctors', methods=['GET'])
def top_doctors():
    """
    Returns the top 3 doctors by average rating.
    Response: [
      {
        "doctor_id": 5,
        "first_name": "Alice",
        "last_name": "Jones",
        "average_rating": 4.8,
        "total_ratings": 12
      },
      …
    ]
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
              d.doctor_id,
              d.first_name,
              d.last_name,
              dr.average_rating,
              dr.total_ratings
            FROM doctor_ratings dr
            JOIN doctors d
              ON dr.doctor_id = d.doctor_id
            ORDER BY dr.average_rating DESC
            LIMIT 3
        """)
        rows = cursor.fetchall()

        # Ensure JSON-serializable types
        top_three = []
        for r in rows:
            top_three.append({
                "doctor_id":            r["doctor_id"],
                "first_name":           r["first_name"],
                "last_name":            r["last_name"],
                "average_rating":       float(r["average_rating"]),
                "total_ratings":        r["total_ratings"]
            })

        return jsonify(top_three), 200

    except mysql.connector.Error as err:
        print("❌ Error fetching top doctors:", err)
        return jsonify(error="Internal server error"), 500

    finally:
        cursor.close()
        conn.close()
