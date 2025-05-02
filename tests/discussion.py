from blueprints.discussion import discussion_bp
import pytest
from flask import Flask
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(discussion_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# test create new post


def test_create_post(client):
    response = client.post('/api/discussion/post', json={
        'doctor_id': 1,
        'post_title': 'Test Title',
        'post_content': {'text': 'Test Content'}
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Post created successfully'

# test get all the posts


def test_get_all_posts(client):
    response = client.get('/api/discussion/posts')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# test get reply


def test_reply_to_post(client):
    response = client.post('/api/discussion/reply', json={
        'post_id': 1,
        'patient_id': 1,
        'reply_content': 'Test Reply'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Reply submitted successfully'

# test get post rply


def test_get_post_replies(client):
    response = client.get('/api/discussion/replies/1')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
