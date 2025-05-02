from blueprints.auth import auth_bp
import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# Testing for missing fields


def test_login_missing_fields(client):
    response = client.post('/api/auth/login', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Missing required fields'

# Test mailbox does not exist


def test_login_invalid_email(client):
    response = client.post('/api/auth/login', json={
        'email': 'doesnotexist123456@example.com',  # Make sure this mailbox doesn't exist
        'password': 'any_password'
    })
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid email or password'

# Test for correct login (based on doctor1@gmail.com)


def test_login_success(client):
    response = client.post('/api/auth/login', json={
        'email': 'dr.house@example.com',  # The real e-mail address in your database.
        'password': 'password'  # The corresponding real password
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert 'user' in data
    assert 'email' in data['user']
    assert data['user']['email'] == 'dr.house@example.com'  # Fix the assertion to be a real mailbox
