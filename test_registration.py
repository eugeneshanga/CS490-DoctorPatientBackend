import json
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello(client):
    response = client.get("/api/hello")
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["message"] == "Hello World!"

# Send a request with missing required fields (e.g., missing password)
def test_register_patient_missing_fields(client):
    payload = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post("/api/register/patient", json=payload)
    json_data = response.get_json()
    assert response.status_code == 400
    assert "Missing required fields" in json_data["error"]

# Use a unique email to avoid duplicate key errors on repeated test runs
def test_register_patient_success(client):
    payload = {
        "email": "uniqueuser@example.com",
        "password": "mypassword",
        "first_name": "Unique",
        "last_name": "User",
        "address": "123 Test St",
        "phone_number": "1234567890",
        "zip_code": "12345"
    }
    response = client.post("/api/register/patient", json=payload)
    json_data = response.get_json()
    assert response.status_code == 201
    assert "Patient registered successfully" in json_data["message"]
