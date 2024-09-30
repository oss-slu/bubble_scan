import os
import pytest
from io import BytesIO
from flask import Flask

@pytest.fixture
def client():
    from app import app  # Import the Flask app from your main app file
    with app.test_client() as client:
        yield client

def test_get_data(client):
    """Test the /api/data route."""
    response = client.get('/api/data')
    assert response.status_code == 200
    assert response.json['message'] == "Hello from Flask!"

def test_receive_message(client):
    """Test the /api/message route."""
    response = client.post('/api/message', json={'message': 'Test Message'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Message received successfully!'

def test_file_upload(client):
    """Test file upload route with a valid PDF file."""
    data = {
        'file': (BytesIO(b"fake_pdf_content"), 'test.pdf')
    }
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert 'file_id' in response.json

def test_invalid_file_upload(client):
    """Test file upload route with an invalid file type."""
    data = {
        'file': (BytesIO(b"fake_text_content"), 'test.txt')
    }
    response = client.post('/api/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Only PDF files are allowed'

def test_download_csv(client):
    """Test downloading CSV from valid file_id."""
    # Mock file data (add logic to mock if necessary)
    valid_file_id = "mock_file_id"
    response = client.get(f'/api/download_csv/{valid_file_id}')
    assert response.status_code == 200  # If file_id is valid
    assert 'attachment' in response.headers['Content-Disposition']
