from blueprints.patientDashboard.payments import patient_dashboard_payments_bp
from flask import Flask
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(patient_dashboard_payments_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# 1. Test to get physician payment records successful


def test_get_doctor_payments_success(client):
    response = client.get('/api/patient-dashboard/payments/doctor?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        payments = response.get_json()
        assert isinstance(payments, list)

# 2. est to get physician payment records missing user_id


def test_get_doctor_payments_missing_user_id(client):
    response = client.get('/api/patient-dashboard/payments/doctor')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'user_id query parameter is required'

# 3.Test to get pharmacy payment records successful


def test_get_pharmacy_payments_success(client):
    response = client.get('/api/patient-dashboard/payments/pharmacy?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        payments = response.get_json()
        assert isinstance(payments, list)

# 4. Test getting pharmacy payment records missing user_id


def test_get_pharmacy_payments_missing_user_id(client):
    response = client.get('/api/patient-dashboard/payments/pharmacy')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'user_id query parameter is required'

# 5. Test getting a user_id for a physician payment record that doesn't exist


def test_get_doctor_payments_invalid_user_id(client):
    response = client.get('/api/patient-dashboard/payments/doctor?user_id=99999')  # make sure id not exit
    assert response.status_code in (404, 200)
    if response.status_code == 404:
        assert response.get_json()['error'] == 'Patient not found for given user_id'
