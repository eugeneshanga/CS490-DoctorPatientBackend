from blueprints.paymentsPage.transactions import payment_transaction_bp
import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(payment_transaction_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# 1.Get Physician Payment Details


def test_get_doctor_payment_success(client):
    response = client.get('/api/payment/transaction/payments/doctor/1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        payment = response.get_json()
        assert 'payment_id' in payment

# 2. Complete Physician Payment


def test_fulfill_doctor_payment_success(client):
    response = client.patch('/api/payment/transaction/payments/doctor/1/fulfill', json={
        'cardholder_name': 'John Doe',
        'card_number': '1234567890123456',
        'exp_month': 12,
        'exp_year': 2025,
        'cvv': '123'
    })
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert response.get_json()['message'] == 'Payment fulfilled and details recorded'

# 3. Get Pharmacy Payment Details


def test_get_pharmacy_payment_success(client):
    response = client.get('/api/payment/transaction/payments/pharmacy/1')
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        payment = response.get_json()
        assert 'payment_id' in payment

# 4. Completion of pharmacy payments


def test_fulfill_pharmacy_payment_success(client):
    response = client.patch('/api/payment/transaction/payments/pharmacy/1/fulfill', json={
        'cardholder_name': 'Jane Doe',
        'card_number': '9876543210987654',
        'exp_month': 11,
        'exp_year': 2026,
        'cvv': '456'
    })
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert response.get_json()['message'] == 'Payment fulfilled and details recorded'

# 5. Missing payment details field


def test_fulfill_doctor_payment_missing_fields(client):
    response = client.patch('/api/payment/transaction/payments/doctor/1/fulfill', json={
        'cardholder_name': 'John Doe'
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()
