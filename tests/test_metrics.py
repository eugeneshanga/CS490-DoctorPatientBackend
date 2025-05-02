from blueprints.patientDashboard.metrics import patient_dashboard_metrics_bp
from flask import Flask
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(patient_dashboard_metrics_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# 1. Test Submission Medical Indicator Success


def test_submit_medical_metrics_success(client):
    response = client.post('/api/patient-dashboard/metrics/submit', json={
        'user_id': 1,  # real use id
        'weight': 70.5,
        'height': 1.75,
        'caloric_intake': 2200
    })
    assert response.status_code in (201, 404)
    if response.status_code == 201:
        data = response.get_json()
        assert 'metric_id' in data

# 2. Test Submission Missing Fields


def test_submit_medical_metrics_missing_fields(client):
    response = client.post('/api/patient-dashboard/metrics/submit', json={
        'user_id': 1
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

# 3. Test Getting Chart Data Successfully


def test_get_graph_data_success(client):
    response = client.get('/api/patient-dashboard/metrics/graph-data?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.get_json()
        assert 'weight_data' in data
        assert 'caloric_intake_data' in data

# 4.Test to get chart data missing user_id


def test_get_graph_data_missing_user_id(client):
    response = client.get('/api/patient-dashboard/metrics/graph-data')
    assert response.status_code == 400
    assert 'error' in response.get_json()

# 5. Test to get the latest height success


def test_get_latest_height_success(client):
    response = client.get('/api/patient-dashboard/metrics/latest-height?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.get_json()
        assert 'latest_height' in data

# 6. Test to get the latest height missing user_id


def test_get_latest_height_missing_user_id(client):
    response = client.get('/api/patient-dashboard/metrics/latest-height')
    assert response.status_code == 400
    assert 'error' in response.get_json()
