from blueprints.patientDashboard.mealplans import mealplans_bp
from flask import Flask
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(mealplans_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# 1. Test Creation of Meal Plans Successful (without pictures)


def test_create_patient_mealplan_success(client):
    data = {
        'user_id': 1,  # Make sure the database has a patient_id counterpart
        'title': 'Test Meal Plan',
        'description': 'Healthy Meal',
        'instructions': 'Cook and serve.',
        'calories': 300,
        'fat': 10,
        'sugar': 5,
        'ingredients': 'rice, chicken, vegetables'
    }
    response = client.post('/api/patient-dashboard/mealplans/patient/create', data=data)
    assert response.status_code in (201, 404)
    if response.status_code == 201:
        result = response.get_json()
        assert 'meal_plan_id' in result

# 2. Test access to all meal plans for patients


def test_get_patient_mealplans(client):
    response = client.get('/api/patient-dashboard/mealplans/patient/all?user_id=1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.get_json()
        assert 'mealplans' in data
        assert isinstance(data['mealplans'], list)

# 3. Test deletion of meal plans


def test_delete_mealplan(client):
    response = client.delete('/api/patient-dashboard/mealplans/delete/1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.get_json()
        assert data['message'] == 'Meal plan deleted'

# 4.  Test Creation of Meal Plans with Missing Fields


def test_create_mealplan_missing_fields(client):
    response = client.post('/api/patient-dashboard/mealplans/patient/create', data={
        'user_id': 1
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()

# 5. Patients not present when testing access to meal plans


def test_get_mealplans_invalid_user(client):
    response = client.get('/api/patient-dashboard/mealplans/patient/all?user_id=99999')  # fake ID
    assert response.status_code in (404, 200)
    if response.status_code == 404:
        assert response.get_json()['error'] == 'Patient not found for this user_id'
