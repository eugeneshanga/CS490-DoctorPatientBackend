from flask import Blueprint, jsonify, request
import mysql.connector
from config import DB_CONFIG

patient_dashboard_bp = Blueprint('patient_dashboard', __name__, url_prefix='/api/patient-dashboard')


@patient_dashboard_bp.route('/details', methods=['GET'])
def get_patient_details():
    """
    Endpoint to retrieve patient details for a given user_id.
    Expects a query parameter 'user_id'. Converts user_id to patient_id,
    then retrieves first_name, last_name, and patient_id from the patients table.
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT patient_id, first_name, last_name FROM patients WHERE user_id = %s",
            (user_id,)
        )
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found for given user_id"}), 404

        cursor.close()
        connection.close()

        return jsonify({"patient": patient}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@patient_dashboard_bp.route('/search-doctors', methods=['GET'])
def search_doctors():
    """
    Endpoint to search for doctors based on a query.
    Returns only the necessary fields: doctor_id, first_name, last_name,
    license_number, and phone_number.
    """
    search_query = request.args.get('query', default='', type=str)

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        if search_query:
            # Use a LIKE query to match the first or last name
            like_query = f"%{search_query}%"
            sql = """
                SELECT doctor_id, first_name, last_name, license_number, phone_number
                FROM doctors
                WHERE is_active = TRUE AND (first_name LIKE %s OR last_name LIKE %s)
            """
            cursor.execute(sql, (like_query, like_query))
        else:
            # If no search term, return all active doctors with selected fields
            sql = """
                SELECT doctor_id, first_name, last_name, license_number, phone_number
                FROM doctors
                WHERE is_active = TRUE
            """
            cursor.execute(sql)

        doctors = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(doctors), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@patient_dashboard_bp.route('/preferred_pharmacy', methods=['GET'])
def get_preferred_pharmacy():
    """
    Endpoint to get a patient's preferred pharmacy based on user_id input
    Returns Pharmacy ID, Name, Address, Zip Code and Phone Number
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify(error="Missing query parameter: user_id"), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Ensure this user is a patient
        cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify(error=f"User {user_id} is not a patient"), 404

        # Lookup preferred pharmacy
        cursor.execute("""
            SELECT ph.pharmacy_id,
                   ph.name,
                   ph.address,
                   ph.zip_code,
                   ph.phone_number
              FROM patient_preferred_pharmacy pp
              JOIN pharmacies ph
                ON pp.pharmacy_id = ph.pharmacy_id
             WHERE pp.patient_id = %s
        """, (patient['patient_id'],))
        pref = cursor.fetchone()
        if not pref:
            return jsonify(error="No preferred pharmacy set"), 404

        return jsonify(pref), 200

    except mysql.connector.Error as err:
        print("❌ Error fetching preferred pharmacy:", err)
        return jsonify(error="Internal server error"), 500

    finally:
        cursor.close()
        conn.close()


@patient_dashboard_bp.route('/meal-plans', methods=['GET'])
def get_meal_plans():
    """
    Endpoint to fetch all meal plans for a given patient.
    Now expects a query parameter `user_id` and then looks up the corresponding patient_id.
    Returns a list of meal plans.
    """
    user_id = request.args.get('user_id', type=int)

    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Convert user_id to patient_id
        cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({"error": "Patient not found for the given user_id"}), 404
        patient_id = patient["patient_id"]

        # Retrieve all meal plans for the patient, ordered by creation date descending
        sql = """
            SELECT meal_plan_id, patient_id, meal_plan, created_at
            FROM patient_meal_plans
            WHERE patient_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(sql, (patient_id,))
        meal_plans = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(meal_plans), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@patient_dashboard_bp.route('/pending-prescriptions', methods=['GET'])
def list_patient_prescriptions():
    """
    Returns all pending prescriptions for the logged‐in patient.
    Query param: user_id
    Response JSON: [
      {
        "prescription_id": 12,
        "drug_id": 3,
        "drug_name": "Ozempic",
        "dosage": "0.5mg",
        "instructions": "Once weekly",
        "status": "pending",
        "requested_at": "2025-04-20 14:23:00"
      },
      …
    ]
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify(error="Missing query param: user_id"), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)

        # 1) resolve patient_id
        cur.execute(
            "SELECT patient_id FROM patients WHERE user_id = %s",
            (user_id,)
        )
        row = cur.fetchone()
        if not row:
            return jsonify(error="Patient not found for this user_id"), 404
        patient_id = row['patient_id']

        # 2) get pending prescriptions
        cur.execute("""
            SELECT
              p.prescription_id,
              p.drug_id,
              d.name AS drug_name,
              p.dosage,
              p.instructions,
              p.status,
              p.created_at AS requested_at
            FROM prescriptions p
            JOIN weight_loss_drugs d ON p.drug_id = d.drug_id
            WHERE p.patient_id = %s
              AND p.status = 'pending'
            ORDER BY p.created_at DESC
        """, (patient_id,))

        prescriptions = cur.fetchall()
        return jsonify(prescriptions), 200

    except mysql.connector.Error as err:
        print(err)
        return jsonify(error="Internal server error"), 500

    finally:
        cur.close()
        conn.close()


@patient_dashboard_bp.route('/prescriptions/filled', methods=['GET'])
def get_filled_prescriptions():
    """
    Return all filled prescriptions for a patient, newest first.
    Query param: ?user_id=<user_id>
    """
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify(error="user_id is required"), 400

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # Look up the patient_id
    cursor.execute(
        "SELECT patient_id FROM patients WHERE user_id = %s",
        (user_id,)
    )
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return jsonify(error="No patient found for that user"), 404
    patient_id = row['patient_id']

    # Fetch all filled prescriptions
    cursor.execute("""
        SELECT
          pr.prescription_id,
          wd.name         AS drug_name,
          pr.dosage,
          pr.instructions,
          pr.status,
          pr.created_at   AS requested_at
        FROM prescriptions pr
        JOIN weight_loss_drugs wd
          ON pr.drug_id = wd.drug_id
        WHERE pr.patient_id = %s
          AND pr.status     = 'filled'
        ORDER BY pr.created_at DESC;
    """, (patient_id,))

    filled = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(filled)
