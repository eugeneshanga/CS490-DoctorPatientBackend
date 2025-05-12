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
