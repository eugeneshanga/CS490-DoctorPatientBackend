from blueprints.doctorDashboard.appointments import doctor_dashboard_appointments_bp
import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(doctor_dashboard_appointments_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# 1. Test Getting Scheduled Reservation Success


def test_get_scheduled_appointments_success(client):
    response = client.get('/api/doctor-dashboard/appointments/?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert isinstance(response.get_json(), list)

# 2. Test respond interface - successfully accepted
def test_respond_to_appointment_accept(client):
    response = client.post('/api/doctor-dashboard/appointments/respond', json={
        'user_id': 1,
        'appointment_id': 1,
        'accepted': True
    })
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert 'message' in response.get_json()

# 3. Test respond interface - missing fields


def test_respond_to_appointment_missing_fields(client):
    response = client.post('/api/doctor-dashboard/appointments/respond', json={
        'user_id': 1
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

# 4. Test access accepted Reservation
def test_get_accepted_appointments(client):
    response = client.get('/api/doctor-dashboard/appointments/accepted?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert isinstance(response.get_json(), list)

# 5.Test getting canceled appointments
def test_get_canceled_appointments(client):
    response = client.get('/api/doctor-dashboard/appointments/canceled?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert isinstance(response.get_json(), list)

# 6. Test Access Completed Reservations
def test_get_completed_appointments(client):
    response = client.get('/api/doctor-dashboard/appointments/completed?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert isinstance(response.get_json(), list)

# 7. Test complete interface
def test_complete_appointment(client):
    response = client.patch('/api/doctor-dashboard/appointments/complete', json={
        'appointment_id': 1
    })
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert 'message' in response.get_json()
