from flask import Blueprint, request, jsonify
from mysql.connector import connect, Error
from config import DB_CONFIG

dashboard_top_end_bp = Blueprint('dashboard_top_end_bp', __name__)


@dashboard_top_end_bp.route('/api/dashboard/user-info', methods=['POST'])
def get_dashboard_user_info():
    try:
        data = request.get_json()
        user_type = data.get('user_type')
        user_id = data.get('user_id')

        print(f"✅ Received request for user_type: {user_type}, user_id: {user_id}")

        if not user_type or not user_id:
            return jsonify({'error': 'Missing user_type or user_id'}), 400

        # Correct table names
        table_map = {
            'patient': 'patients',
            'doctor': 'doctors',
            'pharmacist': 'pharmacies'
        }

        table = table_map.get(user_type)
        if not table:
            return jsonify({'error': 'Invalid user_type'}), 400

        # Build correct query based on user type
        if user_type == 'patient':
            query = "SELECT patient_id, first_name, last_name, address, phone_number FROM patients WHERE patient_id = %s"
        elif user_type == 'doctor':
            query = """
                SELECT 
                    d.doctor_id,
                    d.first_name,
                    d.last_name,
                    d.address,
                    d.phone_number,
                    IFNULL(AVG(r.rating), 0) AS average_rating
                FROM doctors d
                LEFT JOIN ratings r ON d.doctor_id = r.doctor_id
                WHERE d.user_id = %s
                GROUP BY d.doctor_id
            """
        elif user_type == 'pharmacist':
            query = "SELECT pharmacy_id, name, address, phone_number FROM pharmacies WHERE user_id = %s"
        else:
            return jsonify({'error': 'Invalid user_type'}), 400

        print(f"🔍 Running query: {query} with user_id: {user_id}")

        with connect(**DB_CONFIG) as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if result:
                    print(f"📦 Backend is sending back this result: {result}")
                    return jsonify(result), 200
                else:
                    return jsonify({'error': 'User not found'}), 404

    except Error as e:
        print(f"💥 Database error: {e}")
        return jsonify({'error': 'Database connection error'}), 500
    except Exception as e:
        print(f"💥 Internal Server Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@dashboard_top_end_bp.route('/api/dashboard/update-info', methods=['POST'])
def update_user_info():
    data = request.get_json()
    user_type = data.get('user_type')
    user_id = data.get('user_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    address = data.get('address')
    phone_number = data.get('phone_number')

    table_map = {
        'patient': 'patients',
        'doctor': 'doctors',
        'pharmacist': 'pharmacies'
    }

    id_col = f"{user_type}_id"
    table = table_map.get(user_type)

    if not table:
        return jsonify({'error': 'Invalid user type'}), 400

    query = f"""
        UPDATE {table}
        SET first_name = %s,
            last_name = %s,
            address = %s,
            phone_number = %s
        WHERE {id_col} = %s
    """

    try:
        with connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (first_name, last_name, address, phone_number, user_id))
                conn.commit()
        return jsonify({'message': 'User info updated successfully'}), 200
    except Exception as e:
        print("Update error:", e)
        return jsonify({'error': 'Update failed'}), 500
