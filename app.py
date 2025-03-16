from flask import Flask, jsonify
from flask_cors import CORS  # CORS for handling cross-origin requests
import mysql.connector
from config import DB_CONFIG
from blueprints.registration import registration_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(registration_bp)


# First route!
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello World!")


# Display some doctors
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        # Create a connection to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        # dictionary=True returns rows as dicts with column names as keys

        # Example query: retrieving all doctors
        cursor.execute("SELECT * FROM doctors")
        rows = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return the data as JSON
        return jsonify(rows), 200

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({"error": str(err)}), 500


if __name__ == '__main__':
    app.run(debug=True)
