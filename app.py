from flask import Flask, jsonify
from flask_cors import CORS  # CORS for handling cross-origin requests
import mysql.connector
from config import DB_CONFIG
from blueprints.landingPage.landingPage import pharmacy_bp
from blueprints.landingPage.landingPage import doctor_bp
from blueprints.registration import registration_bp
from blueprints.dashboardTopEnd.dashboardTopEnd import dashboard_top_end_bp
from blueprints.patientDashboard.dashboard import patient_dashboard_bp
from blueprints.patientDashboard.payments import patient_dashboard_payments_bp
from blueprints.patientDashboard.appointments import patient_dashboard_appointments_bp
from blueprints.patientDashboard.metrics import patient_dashboard_metrics_bp
from blueprints.auth import auth_bp
from blueprints.discussion import discussion_bp
from blueprints.doctorDashboard.dashboard import doctor_dashboard_bp
from blueprints.doctorDashboard.payments import doctor_dashboard_payments_bp
from blueprints.doctorDashboard.appointments import doctor_dashboard_appointments_bp
from blueprints.patientDashboard.mealplans import mealplans_bp
from blueprints.doctorDashboard.mealPlans import doctor_mealplans_bp
from blueprints.paymentsPage.transactions import payment_transaction_bp
from blueprints.chat import chat_bp
from blueprints.postAppointment.results import results_bp
from blueprints.postAppointment.ratings import ratings_bp
from blueprints.doctorReviews.getDoctorReviews import reviews_bp

import os

app = Flask(__name__)


@app.route('/debug-images')
def debug_images():
    files = os.listdir('static/images')
    return '<br>'.join(files)


app = Flask(__name__)
CORS(app)

app.register_blueprint(pharmacy_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(registration_bp)
app.register_blueprint(dashboard_top_end_bp)
app.register_blueprint(patient_dashboard_bp)
app.register_blueprint(patient_dashboard_payments_bp)
app.register_blueprint(patient_dashboard_appointments_bp)
app.register_blueprint(patient_dashboard_metrics_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(discussion_bp)
app.register_blueprint(doctor_dashboard_bp)
app.register_blueprint(doctor_dashboard_payments_bp)
app.register_blueprint(doctor_dashboard_appointments_bp)
app.register_blueprint(mealplans_bp)
app.register_blueprint(doctor_mealplans_bp)
app.register_blueprint(payment_transaction_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(results_bp)
app.register_blueprint(ratings_bp)
app.register_blueprint(reviews_bp)


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
