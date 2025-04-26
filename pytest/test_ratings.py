from blueprints.postAppointment.ratings import ratings_bp
from flask import Flask
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(ratings_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# 1. Test successfully submitted for grading


def test_rate_doctor_success(client):
    response = client.post('/api/post-appointment/ratings/rate_doctor', json={
        'patient_id': 1,
        'doctor_id': 1,
        'appointment_id': 1,
        'rating': 4.5,
        'review': 'Great doctor!'
    })
    assert response.status_code in (201, 404, 403, 409)

# 2. Test for missing required fields


def test_rate_doctor_missing_fields(client):
    response = client.post('/api/post-appointment/ratings/rate_doctor', json={
        'doctor_id': 1,
        'rating': 4
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

# 3. Test scores out of range


def test_rate_doctor_invalid_rating(client):
    response = client.post('/api/post-appointment/ratings/rate_doctor', json={
        'patient_id': 1,
        'doctor_id': 1,
        'appointment_id': 1,
        'rating': 6  # Invalid rating
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

# 4. Test Repeat Scoring


def test_rate_doctor_duplicate(client):
    response = client.post('/api/post-appointment/ratings/rate_doctor', json={
        'patient_id': 1,
        'doctor_id': 1,
        'appointment_id': 1,
        'rating': 5
    })
    # Run twice, first 201, second should 409
    if response.status_code == 201:
        response2 = client.post('/api/post-appointment/ratings/rate_doctor', json={
            'patient_id': 1,
            'doctor_id': 1,
            'appointment_id': 1,
            'rating': 5
        })
        assert response2.status_code == 409

# 5. Testing Non-JSON Requests


def test_rate_doctor_non_json(client):
    response = client.post('/api/post-appointment/ratings/rate_doctor', data="plain text")
    assert response.status_code == 400
    assert 'error' in response.get_json()
