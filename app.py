from flask import Flask, jsonify
from flask_cors import CORS  # CORS for handling cross-origin requests
import mysql.connector
from config import DB_CONFIG
from blueprints.registration import registration_bp
from blueprints.patientDashboard.dashboard import patient_dashboard_bp
from blueprints.patientDashboard.payments import patient_dashboard_payments_bp
from blueprints.patientDashboard.appointments import patient_dashboard_appointments_bp
from blueprints.patientDashboard.metrics import patient_dashboard_metrics_bp
from blueprints.auth import auth_bp
from blueprints.discussion import discussion_bp
from blueprints.doctorDashboard.dashboard import doctor_dashboard_bp
from blueprints.doctorDashboard.payments import doctor_dashboard_payments_bp
from blueprints.doctorDashboard.appointments import doctor_dashboard_appointments_bp
from blueprints.pharmacyDashboard.dashboard import pharmacy_dashboard_bp
from blueprints.pharmacyDashboard.inventory import pharmacy_inventory_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(registration_bp)
app.register_blueprint(patient_dashboard_bp)
app.register_blueprint(patient_dashboard_payments_bp)
app.register_blueprint(patient_dashboard_appointments_bp)
app.register_blueprint(patient_dashboard_metrics_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(discussion_bp)
app.register_blueprint(doctor_dashboard_bp)
app.register_blueprint(doctor_dashboard_payments_bp)
app.register_blueprint(doctor_dashboard_appointments_bp)
app.register_blueprint(pharmacy_dashboard_bp)
app.register_blueprint(pharmacy_inventory_bp)

if __name__ == '__main__':
    app.run(debug=True)
