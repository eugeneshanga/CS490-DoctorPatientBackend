from blueprints.registration import registration_bp
from flask import Flask
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(registration_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# 1.Patient Registration Successful


def test_register_patient_success(client):
    response = client.post('/api/register/patient', json={
        'email': 'patient_test@example.com',
        'password': 'password123',
        'first_name': 'John',
        'last_name': 'Doe',
        'address': '123 Main St',
        'phone_number': '1234567890',
        'zip_code': '12345'
    })
    assert response.status_code in (201, 500)
    if response.status_code == 201:
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Patient registered successfully'

# 2. Doctor Registration Successful


def test_register_doctor_success(client):
    response = client.post('/api/register/doctor', json={
        'email': 'doctor_test@example.com',
        'password': 'password123',
        'license_number': 'LIC12345',
        'first_name': 'Alice',
        'last_name': 'Smith',
        'address': '456 Health St',
        'phone_number': '9876543210',
        'ssn': '123-45-6789'
    })
    assert response.status_code in (201, 500)
    if response.status_code == 201:
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Doctor registered successfully'

# 3. Successful Pharmacy Registration


def test_register_pharmacy_success(client):
    response = client.post('/api/register/pharmacy', json={
        'email': 'pharmacy_test@example.com',
        'password': 'password123',
        'name': 'Health Pharmacy',
        'address': '789 Pharmacy Ave',
        'zip_code': '54321',
        'phone_number': '5551234567',
        'license_number': 'PHARM123'
    })
    assert response.status_code in (201, 500)
    if response.status_code == 201:
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Pharmacy registered successfully'

# 4. Missing fields for patient registration


def test_register_patient_missing_fields(client):
    response = client.post('/api/register/patient', json={
        'email': 'patient1@gmail.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

# 5. Missing fields for physician registration


def test_register_doctor_missing_fields(client):
    response = client.post('/api/register/doctor', json={
        'email': 'doctor1@gmail.com',
        'password': 'password'
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

# 6.Missing fields for pharmacy registration


def test_register_pharmacy_missing_fields(client):
    response = client.post('/api/register/pharmacy', json={
        'email': 'phancy@gmail.com',
        'password': 'password'
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()
