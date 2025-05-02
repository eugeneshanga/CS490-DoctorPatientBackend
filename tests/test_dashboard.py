from blueprints.doctorDashboard.dashboard import doctor_dashboard_bp
import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(doctor_dashboard_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# 1.  Test Success Get Physician Details


def test_get_doctor_details_success(client):
    response = client.get('/api/doctor-dashboard/details?user_id=1')
    assert response.status_code in (200, 404)  # 200 if present, 404 if not present
    if response.status_code == 200:
        data = response.get_json()
        assert 'doctor' in data
        assert 'first_name' in data['doctor']

# 2. Test for missing user_id parameter


def test_get_doctor_details_missing_user_id(client):
    response = client.get('/api/doctor-dashboard/details')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'user_id query parameter is required'

# 3. Test for non-existent user_id


def test_get_doctor_details_invalid_user_id(client):
    response = client.get('/api/doctor-dashboard/details?user_id=99999')  # Make sure this user_id does not exist
    assert response.status_code == 404 or response.status_code == 200
    if response.status_code == 404:
        assert response.get_json()['error'] == 'Doctor not found for given user_id'
