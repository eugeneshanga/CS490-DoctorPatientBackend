from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

pharmacy_inventory_bp = Blueprint('pharmacy_inventory', __name__, url_prefix='/api/pharmacy-dashboard/inventory')


@pharmacy_inventory_bp.route('/contents', methods=['GET'])
def get_inventory():
    """
    Endpoint to retrieve the current pharmacy inventory.
    Expects a query parameter 'user_id', converts it to pharmacy_id,
    then retrieves all inventory items (inventory_id, pharmacy_id, drug_name, stock_quantity)
    for that pharmacy.
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to pharmacy_id
        cursor.execute("SELECT pharmacy_id FROM pharmacies WHERE user_id = %s", (user_id,))
        pharmacy = cursor.fetchone()
        if not pharmacy:
            return jsonify({"error": "Pharmacy not found for given user_id"}), 404
        pharmacy_id = pharmacy["pharmacy_id"]

        # Query the pharmacy_inventory table for this pharmacy's inventory
        sql = """
            SELECT inventory_id, pharmacy_id, drug_name, stock_quantity
            FROM pharmacy_inventory
            WHERE pharmacy_id = %s
            ORDER BY drug_name ASC
        """
        cursor.execute(sql, (pharmacy_id,))
        inventory = cursor.fetchall()

        cursor.close()
        connection.close()
        return jsonify(inventory), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
