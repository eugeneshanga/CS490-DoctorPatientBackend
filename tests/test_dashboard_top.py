from blueprints.dashboardTopEnd.dashboardTopEnd import dashboard_top_end_bp
import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(dashboard_top_end_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# Testing the user-info interface - successfully obtained


def test_get_dashboard_user_info_success(client):
    response = client.post('/api/dashboard/user-info', json={
        'user_type': 'doctor',
        'user_id': 1  # Ensure that the database has
    })
    assert response.status_code in (200, 404)  # 200 if present, 404 if not present
    if response.status_code == 200:
        data = response.get_json()
        assert 'first_name' in data
        assert 'last_name' in data

# Testing the user-info interface - missing fields


def test_get_dashboard_user_info_missing_fields(client):
    response = client.post('/api/dashboard/user-info', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Missing user_type or user_id'

# Testing the user-info interface - error user_type


def test_get_dashboard_user_info_invalid_user_type(client):
    response = client.post('/api/dashboard/user-info', json={
        'user_type': 'invalid_type',
        'user_id': 1
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid user_type'

# Testing the update-info interface - successful update


def test_update_user_info_success(client):
    response = client.post('/api/dashboard/update-info', json={
        'user_type': 'doctor',
        'user_id': 1,  # Ensure that the database has
        'first_name': 'Updated',
        'last_name': 'Doctor',
        'address': '123 Updated St',
        'phone_number': '1234567890'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User info updated successfully'

# Testing update-info interface - error user_type


def test_update_user_info_invalid_user_type(client):
    response = client.post('/api/dashboard/update-info', json={
        'user_type': 'invalid_type',
        'user_id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'address': '123 Main St',
        'phone_number': '1234567890'
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid user type'
